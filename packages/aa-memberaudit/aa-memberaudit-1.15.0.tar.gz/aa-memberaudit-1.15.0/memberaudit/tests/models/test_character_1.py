import datetime as dt
import hashlib
import json
from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils.timezone import now
from esi.errors import TokenError
from esi.models import Token
from eveuniverse.models import EveEntity, EveMarketPrice, EveSolarSystem, EveType

from app_utils.testing import NoSocketsTestCase, create_user_from_evecharacter

from ...models import (
    Character,
    CharacterContract,
    CharacterContractItem,
    CharacterShip,
    CharacterSkill,
    CharacterSkillqueueEntry,
    CharacterUpdateStatus,
    CharacterWalletJournalEntry,
    Location,
    SkillSet,
    SkillSetGroup,
    SkillSetSkill,
)
from ..testdata.factories import create_character, create_character_update_status
from ..testdata.load_entities import load_entities
from ..testdata.load_eveuniverse import load_eveuniverse
from ..testdata.load_locations import load_locations
from ..utils import (
    add_memberaudit_character_to_user,
    create_memberaudit_character,
    scope_names_set,
)

MODELS_PATH = "memberaudit.models"
MANAGERS_PATH = "memberaudit.managers"
TASKS_PATH = "memberaudit.tasks"


class TestCharacter(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()

    def setUp(self) -> None:
        self.character_1001 = create_memberaudit_character(1001)
        self.user = self.character_1001.character_ownership.user

    def test_is_main_1(self):
        self.assertTrue(self.character_1001.is_main)

    def test_is_main_2(self):
        character_1101 = add_memberaudit_character_to_user(self.user, 1101)
        self.assertTrue(self.character_1001.is_main)
        self.assertFalse(character_1101.is_main)

    def test_is_main_3(self):
        self.user.profile.main_character = None
        self.user.profile.save()
        self.assertFalse(self.character_1001.is_main)

    def test_should_keep_sharing(self):
        # given
        _, character_ownership = create_user_from_evecharacter(
            1001,
            permissions=["memberaudit.basic_access", "memberaudit.share_characters"],
        )
        character = create_character(
            character_ownership=character_ownership, is_shared=True
        )
        # when
        character.update_sharing_consistency()
        # then
        character.refresh_from_db()
        self.assertTrue(character.is_shared)

    def test_should_remove_sharing(self):
        # given
        _, character_ownership = create_user_from_evecharacter(
            1001,
            permissions=["memberaudit.basic_access"],
        )
        character = create_character(
            character_ownership=character_ownership, is_shared=True
        )
        # when
        character.update_sharing_consistency()
        # then
        character.refresh_from_db()
        self.assertFalse(character.is_shared)


class TestCharacterContract(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_eveuniverse()
        load_entities()
        load_locations()
        cls.character_1001 = create_memberaudit_character(1001)
        cls.character_1002 = create_memberaudit_character(1002)
        cls.token = cls.character_1001.character_ownership.user.token_set.first()
        cls.jita = EveSolarSystem.objects.get(id=30000142)
        cls.jita_44 = Location.objects.get(id=60003760)
        cls.amamake = EveSolarSystem.objects.get(id=30002537)
        cls.structure_1 = Location.objects.get(id=1000000000001)
        cls.item_type_1 = EveType.objects.get(id=19540)
        cls.item_type_2 = EveType.objects.get(id=19551)

    def setUp(self) -> None:
        self.contract = CharacterContract.objects.create(
            character=self.character_1001,
            contract_id=42,
            availability=CharacterContract.AVAILABILITY_PERSONAL,
            contract_type=CharacterContract.TYPE_ITEM_EXCHANGE,
            date_issued=now(),
            date_expired=now() + dt.timedelta(days=3),
            for_corporation=False,
            issuer=EveEntity.objects.get(id=1001),
            issuer_corporation=EveEntity.objects.get(id=2001),
            status=CharacterContract.STATUS_OUTSTANDING,
            start_location=self.jita_44,
            end_location=self.jita_44,
        )
        self.contract_completed = CharacterContract.objects.create(
            character=self.character_1001,
            contract_id=43,
            availability=CharacterContract.AVAILABILITY_PERSONAL,
            contract_type=CharacterContract.TYPE_ITEM_EXCHANGE,
            date_issued=now() - dt.timedelta(days=3),
            date_completed=now() - dt.timedelta(days=2),
            date_expired=now() - dt.timedelta(days=1),
            for_corporation=False,
            issuer=EveEntity.objects.get(id=1001),
            issuer_corporation=EveEntity.objects.get(id=2001),
            status=CharacterContract.STATUS_FINISHED,
            start_location=self.jita_44,
            end_location=self.jita_44,
        )

    def test_str(self):
        self.assertEqual(str(self.contract), f"{self.character_1001}-42")

    def test_is_completed(self):
        self.assertFalse(self.contract.is_completed)
        self.assertTrue(self.contract_completed.is_completed)

    def test_has_expired(self):
        self.assertFalse(self.contract.has_expired)
        self.assertTrue(self.contract_completed.has_expired)

    def test_hours_issued_2_completed(self):
        self.assertIsNone(self.contract.hours_issued_2_completed)
        self.assertEqual(self.contract_completed.hours_issued_2_completed, 24)

    def test_summary_one_item_1(self):
        CharacterContractItem.objects.create(
            contract=self.contract,
            record_id=1,
            is_included=True,
            is_singleton=False,
            quantity=1,
            eve_type=self.item_type_1,
        )
        self.assertEqual(self.contract.summary(), "High-grade Snake Alpha")

    def test_summary_one_item_2(self):
        CharacterContractItem.objects.create(
            contract=self.contract,
            record_id=1,
            is_included=True,
            is_singleton=False,
            quantity=1,
            eve_type=self.item_type_1,
        )
        CharacterContractItem.objects.create(
            contract=self.contract,
            record_id=2,
            is_included=False,
            is_singleton=False,
            quantity=1,
            eve_type=self.item_type_2,
        )
        self.assertEqual(self.contract.summary(), "High-grade Snake Alpha")

    def test_summary_multiple_item(self):
        CharacterContractItem.objects.create(
            contract=self.contract,
            record_id=1,
            is_included=True,
            is_singleton=False,
            quantity=1,
            eve_type=self.item_type_1,
        ),
        CharacterContractItem.objects.create(
            contract=self.contract,
            record_id=2,
            is_included=True,
            is_singleton=False,
            quantity=1,
            eve_type=self.item_type_2,
        )
        self.assertEqual(self.contract.summary(), "[Multiple Items]")

    def test_summary_no_items(self):
        self.assertEqual(self.contract.summary(), "(no items)")

    def test_can_calculate_pricing_1(self):
        """calculate price and total for normal item"""
        CharacterContractItem.objects.create(
            contract=self.contract,
            record_id=1,
            is_included=True,
            is_singleton=False,
            quantity=2,
            eve_type=self.item_type_1,
        ),
        EveMarketPrice.objects.create(eve_type=self.item_type_1, average_price=5000000)
        qs = self.contract.items.annotate_pricing()
        item_1 = qs.get(record_id=1)
        self.assertEqual(item_1.price, 5000000)
        self.assertEqual(item_1.total, 10000000)

    def test_can_calculate_pricing_2(self):
        """calculate price and total for BPO"""
        CharacterContractItem.objects.create(
            contract=self.contract,
            record_id=1,
            is_included=True,
            is_singleton=False,
            quantity=1,
            raw_quantity=-2,
            eve_type=self.item_type_1,
        ),
        EveMarketPrice.objects.create(eve_type=self.item_type_1, average_price=5000000)
        qs = self.contract.items.annotate_pricing()
        item_1 = qs.get(record_id=1)
        self.assertIsNone(item_1.price)
        self.assertIsNone(item_1.total)


class TestCharacterFetchToken(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()

    def setUp(self) -> None:
        self.character = create_memberaudit_character(1001)

    def test_defaults(self):
        token = self.character.fetch_token()
        self.assertIsInstance(token, Token)
        self.assertSetEqual(scope_names_set(token), set(Character.get_esi_scopes()))

    def test_specified_scope(self):
        token = self.character.fetch_token("esi-mail.read_mail.v1")
        self.assertIsInstance(token, Token)
        self.assertIn("esi-mail.read_mail.v1", scope_names_set(token))

    @patch(MODELS_PATH + ".character.notify_throttled")
    def test_should_raise_exception_and_notify_user_if_not_found(
        self, mock_notify_throttled
    ):
        # when
        with self.assertRaises(TokenError):
            self.character.fetch_token("invalid_scope")
        # then
        self.assertTrue(mock_notify_throttled.called)
        _, kwargs = mock_notify_throttled.call_args
        self.assertEqual(kwargs["user"], self.character.character_ownership.user)


class TestCharacterSkillQueue(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_eveuniverse()
        load_entities()
        load_locations()
        cls.character_1001 = create_memberaudit_character(1001)
        cls.skill_type_1 = EveType.objects.get(id=24311)
        cls.skill_type_2 = EveType.objects.get(id=24312)

    def test_is_active_1(self):
        """when training is active and skill is in first position then return True"""
        entry = CharacterSkillqueueEntry.objects.create(
            character=self.character_1001,
            eve_type=self.skill_type_1,
            finish_date=now() + dt.timedelta(days=3),
            finished_level=5,
            queue_position=0,
            start_date=now() - dt.timedelta(days=1),
        )
        self.assertTrue(entry.is_active)

    def test_is_active_2(self):
        """when training is active and skill is not in first position then return False"""
        entry = CharacterSkillqueueEntry.objects.create(
            character=self.character_1001,
            eve_type=self.skill_type_1,
            finish_date=now() + dt.timedelta(days=3),
            finished_level=5,
            queue_position=1,
            start_date=now() - dt.timedelta(days=1),
        )
        self.assertFalse(entry.is_active)

    def test_is_active_3(self):
        """when training is not active and skill is in first position then return False"""
        entry = CharacterSkillqueueEntry.objects.create(
            character=self.character_1001,
            eve_type=self.skill_type_1,
            finished_level=5,
            queue_position=0,
        )
        self.assertFalse(entry.is_active)


class TestCharacterShip(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_eveuniverse()
        load_entities()
        cls.character_1001 = create_memberaudit_character(1001)
        cls.user = cls.character_1001.character_ownership.user

    def test_str(self):
        # given
        CharacterShip.objects.create(
            character=self.character_1001, eve_type=EveType.objects.get(id=603)
        )
        # when
        result = str(self.character_1001.ship)
        # then
        self.assertIn("Bruce Wayne", result)
        self.assertIn("Merlin", result)


class TestCharacterUpdateSection(NoSocketsTestCase):
    def test_method_name(self):
        result = Character.UpdateSection.method_name(
            Character.UpdateSection.CORPORATION_HISTORY
        )
        self.assertEqual(result, "update_corporation_history")

        with self.assertRaises(ValueError):
            result = Character.UpdateSection.method_name("invalid")

    def test_display_name(self):
        result = Character.UpdateSection.display_name(
            Character.UpdateSection.CORPORATION_HISTORY
        )
        self.assertEqual(result, "corporation history")

        with self.assertRaises(ValueError):
            result = Character.UpdateSection.display_name("invalid")


class TestCharacterUpdateStatus(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        cls.character_1001 = create_memberaudit_character(1001)
        cls.content = {"alpha": 1, "bravo": 2}

    def test_str(self):
        # given
        status = create_character_update_status(
            character=self.character_1001, section=Character.UpdateSection.ASSETS
        )
        # when/then
        self.assertEqual(str(status), f"{self.character_1001}-assets")

    def test_reset_1(self):
        # given
        status = create_character_update_status(
            character=self.character_1001,
            is_success=True,
            last_error_message="abc",
            root_task_id="a",
            parent_task_id="b",
        )
        # when
        status.reset()
        # then
        status.refresh_from_db()
        self.assertIsNone(status.is_success)
        self.assertEqual(status.last_error_message, "")
        self.assertEqual(status.root_task_id, "")
        self.assertEqual(status.parent_task_id, "")

    def test_reset_2(self):
        # given
        status = create_character_update_status(
            character=self.character_1001,
            is_success=True,
            last_error_message="abc",
            root_task_id="a",
            parent_task_id="b",
        )
        # when
        status.reset(root_task_id="1", parent_task_id="2")
        # then
        status.refresh_from_db()
        self.assertIsNone(status.is_success)
        self.assertEqual(status.last_error_message, "")
        self.assertEqual(status.root_task_id, "1")
        self.assertEqual(status.parent_task_id, "2")

    def test_has_changed_1(self):
        """When hash is different, then return True"""
        status = create_character_update_status(
            character=self.character_1001, content_hash_1="abc"
        )
        self.assertTrue(status.has_changed(self.content))

    def test_has_changed_2(self):
        """When no hash exists, then return True"""
        status = create_character_update_status(
            character=self.character_1001, content_hash_1=""
        )
        self.assertTrue(status.has_changed(self.content))

    def test_has_changed_3a(self):
        """When hash is equal, then return False"""
        status = create_character_update_status(
            character=self.character_1001,
            content_hash_1=hashlib.md5(
                json.dumps(self.content).encode("utf-8")
            ).hexdigest(),
        )
        self.assertFalse(status.has_changed(self.content))

    def test_has_changed_3b(self):
        """When hash is equal, then return False"""
        status = create_character_update_status(
            character=self.character_1001,
            content_hash_2=hashlib.md5(
                json.dumps(self.content).encode("utf-8")
            ).hexdigest(),
        )
        self.assertFalse(status.has_changed(content=self.content, hash_num=2))

    def test_has_changed_3c(self):
        """When hash is equal, then return False"""
        status = create_character_update_status(
            character=self.character_1001,
            content_hash_3=hashlib.md5(
                json.dumps(self.content).encode("utf-8")
            ).hexdigest(),
        )
        self.assertFalse(status.has_changed(content=self.content, hash_num=3))

    def test_is_updating_1(self):
        """When started_at exist and finished_at does not exist, return True"""
        status = create_character_update_status(
            character=self.character_1001, started_at=now(), finished_at=None
        )
        self.assertTrue(status.is_updating)

    def test_is_updating_2(self):
        """When started_at and finished_at does not exist, return False"""
        status = create_character_update_status(
            character=self.character_1001, started_at=None, finished_at=None
        )
        self.assertFalse(status.is_updating)


class TestCharacterUpdateSectionMethods(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        cls.character_1001 = create_memberaudit_character(1001)
        cls.section = Character.UpdateSection.ASSETS
        cls.content = {"alpha": 1, "bravo": 2}

    def test_reset_1(self):
        """when section exists, reset it"""
        CharacterUpdateStatus.objects.create(
            character=self.character_1001,
            section=self.section,
            is_success=False,
            last_error_message="abc",
        )

        section = self.character_1001.reset_update_section(self.section)

        self.assertIsNone(section.is_success)
        self.assertEqual(section.last_error_message, "")

    def test_reset_2(self):
        """when section does not exist, then create it"""
        section = self.character_1001.reset_update_section(self.section)

        self.assertIsNone(section.is_success)
        self.assertEqual(section.last_error_message, "")

    def test_has_changed_1a(self):
        """When section exists, then return result from has_changed"""
        section = CharacterUpdateStatus.objects.create(
            character=self.character_1001,
            section=self.section,
            is_success=True,
            content_hash_1=hashlib.md5(
                json.dumps(self.content).encode("utf-8")
            ).hexdigest(),
        )
        self.assertEqual(
            self.character_1001.has_section_changed(
                section=self.section, content=self.content
            ),
            section.has_changed(self.content),
        )

    def test_has_changed_1b(self):
        """When section exists, then return result from has_changed"""
        section = CharacterUpdateStatus.objects.create(
            character=self.character_1001,
            section=self.section,
            is_success=True,
            content_hash_2=hashlib.md5(
                json.dumps(self.content).encode("utf-8")
            ).hexdigest(),
        )
        self.assertEqual(
            self.character_1001.has_section_changed(
                section=self.section, content=self.content, hash_num=2
            ),
            section.has_changed(self.content, hash_num=2),
        )

    def test_has_changed_1c(self):
        """When section exists, then return result from has_changed"""
        section = CharacterUpdateStatus.objects.create(
            character=self.character_1001,
            section=self.section,
            is_success=True,
            content_hash_3=hashlib.md5(
                json.dumps(self.content).encode("utf-8")
            ).hexdigest(),
        )
        self.assertEqual(
            self.character_1001.has_section_changed(
                section=self.section, content=self.content, hash_num=3
            ),
            section.has_changed(self.content, hash_num=3),
        )

    def test_has_changed_2(self):
        """When section does not exist, then return True"""
        self.assertTrue(
            self.character_1001.has_section_changed(
                section=self.section, content=self.content
            )
        )

    def test_is_updating_1(self):
        """When section exists, then return result from is_updating"""
        section = CharacterUpdateStatus.objects.create(
            character=self.character_1001, section=self.section, started_at=now()
        )
        self.assertEqual(
            self.character_1001.is_section_updating(section=self.section),
            section.is_updating,
        )

    def test_is_updating_2(self):
        """When section does not exist, then return False"""
        self.assertTrue(self.character_1001.is_section_updating(section=self.section))


@patch(MODELS_PATH + ".character.MEMBERAUDIT_UPDATE_STALE_RING_3", 640)
class TestCharacterIsUpdateSectionStale(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        cls.section = Character.UpdateSection.ASSETS

    def setUp(self) -> None:
        self.character = create_memberaudit_character(1001)

    def test_recently_updated_successfully(self):
        """When section has been recently updated successfully then return False"""
        CharacterUpdateStatus.objects.create(
            character=self.character,
            section=self.section,
            is_success=True,
            started_at=now() - dt.timedelta(seconds=30),
            finished_at=now(),
        )
        self.assertFalse(self.character.is_update_section_stale(self.section))

    def test_recently_updated_unsuccessfully(self):
        """When section has been recently updated, but with errors then return True"""
        CharacterUpdateStatus.objects.create(
            character=self.character, section=self.section, is_success=False
        )
        self.assertTrue(self.character.is_update_section_stale(self.section))

    def test_update_long_ago(self):
        """When section has not been recently updated, then return True"""
        mocked_update_at = now() - dt.timedelta(hours=12)
        with patch("django.utils.timezone.now", Mock(return_value=mocked_update_at)):
            CharacterUpdateStatus.objects.create(
                character=self.character, section=self.section, is_success=True
            )
        self.assertTrue(self.character.is_update_section_stale(self.section))

    def test_does_not_exist(self):
        """When section does not exist, then return True"""
        self.assertTrue(self.character.is_update_section_stale(self.section))


class TestCharacterUpdateSkillSets(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_eveuniverse()
        load_entities()
        load_locations()
        cls.character = create_memberaudit_character(1001)
        cls.skill_type_1 = EveType.objects.get(id=24311)
        cls.skill_type_2 = EveType.objects.get(id=24312)

    def test_has_all_skills(self):
        CharacterSkill.objects.create(
            character=self.character,
            eve_type=self.skill_type_1,
            active_skill_level=5,
            skillpoints_in_skill=10,
            trained_skill_level=5,
        )
        CharacterSkill.objects.create(
            character=self.character,
            eve_type=self.skill_type_2,
            active_skill_level=5,
            skillpoints_in_skill=10,
            trained_skill_level=5,
        )
        skill_set = SkillSet.objects.create(name="Ship 1")
        SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_1, required_level=5
        )
        SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_2, required_level=3
        )
        skill_set_group = SkillSetGroup.objects.create(name="Dummy")
        skill_set_group.skill_sets.add(skill_set)

        self.character.update_skill_sets()

        self.assertEqual(self.character.skill_set_checks.count(), 1)
        first = self.character.skill_set_checks.first()
        self.assertEqual(first.skill_set.pk, skill_set.pk)
        self.assertEqual(first.failed_required_skills.count(), 0)

    def test_one_skill_below(self):
        CharacterSkill.objects.create(
            character=self.character,
            eve_type=self.skill_type_1,
            active_skill_level=5,
            skillpoints_in_skill=10,
            trained_skill_level=5,
        )
        CharacterSkill.objects.create(
            character=self.character,
            eve_type=self.skill_type_2,
            active_skill_level=2,
            skillpoints_in_skill=10,
            trained_skill_level=5,
        )
        skill_set = SkillSet.objects.create(name="Ship 1")
        SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_1, required_level=5
        )
        skill_2 = SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_2, required_level=3
        )
        skill_set_group = SkillSetGroup.objects.create(name="Dummy")
        skill_set_group.skill_sets.add(skill_set)

        self.character.update_skill_sets()

        self.assertEqual(self.character.skill_set_checks.count(), 1)
        first = self.character.skill_set_checks.first()
        self.assertEqual(first.skill_set.pk, skill_set.pk)
        self.assertEqual(
            {obj.pk for obj in first.failed_required_skills.all()}, {skill_2.pk}
        )

    def test_misses_one_skill(self):
        CharacterSkill.objects.create(
            character=self.character,
            eve_type=self.skill_type_1,
            active_skill_level=5,
            skillpoints_in_skill=10,
            trained_skill_level=5,
        )
        skill_set = SkillSet.objects.create(name="Ship 1")
        SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_1, required_level=5
        )
        skill_2 = SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_2, required_level=3
        )
        skill_set_group = SkillSetGroup.objects.create(name="Dummy")
        skill_set_group.skill_sets.add(skill_set)

        self.character.update_skill_sets()

        self.assertEqual(self.character.skill_set_checks.count(), 1)
        first = self.character.skill_set_checks.first()
        self.assertEqual(first.skill_set.pk, skill_set.pk)
        self.assertEqual(
            {obj.pk for obj in first.failed_required_skills.all()}, {skill_2.pk}
        )

    def test_passed_required_and_misses_recommendend_skill(self):
        CharacterSkill.objects.create(
            character=self.character,
            eve_type=self.skill_type_1,
            active_skill_level=4,
            skillpoints_in_skill=10,
            trained_skill_level=4,
        )
        skill_set = SkillSet.objects.create(name="Ship 1")
        skill_1 = SkillSetSkill.objects.create(
            skill_set=skill_set,
            eve_type=self.skill_type_1,
            required_level=3,
            recommended_level=5,
        )
        self.character.update_skill_sets()

        self.assertEqual(self.character.skill_set_checks.count(), 1)
        first = self.character.skill_set_checks.first()
        self.assertEqual(first.skill_set.pk, skill_set.pk)
        self.assertEqual({obj.pk for obj in first.failed_required_skills.all()}, set())
        self.assertEqual(
            {obj.pk for obj in first.failed_recommended_skills.all()}, {skill_1.pk}
        )

    def test_misses_recommendend_skill_only(self):
        CharacterSkill.objects.create(
            character=self.character,
            eve_type=self.skill_type_1,
            active_skill_level=4,
            skillpoints_in_skill=10,
            trained_skill_level=4,
        )
        skill_set = SkillSet.objects.create(name="Ship 1")
        skill_1 = SkillSetSkill.objects.create(
            skill_set=skill_set,
            eve_type=self.skill_type_1,
            recommended_level=5,
        )
        self.character.update_skill_sets()

        self.assertEqual(self.character.skill_set_checks.count(), 1)
        first = self.character.skill_set_checks.first()
        self.assertEqual(first.skill_set.pk, skill_set.pk)
        self.assertEqual({obj.pk for obj in first.failed_required_skills.all()}, set())
        self.assertEqual(
            {obj.pk for obj in first.failed_recommended_skills.all()}, {skill_1.pk}
        )

    def test_misses_all_skills(self):
        skill_set = SkillSet.objects.create(name="Ship 1")
        skill_1 = SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_1, required_level=5
        )
        skill_2 = SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_2, required_level=3
        )
        skill_set_group = SkillSetGroup.objects.create(name="Dummy")
        skill_set_group.skill_sets.add(skill_set)

        self.character.update_skill_sets()

        self.assertEqual(self.character.skill_set_checks.count(), 1)
        first = self.character.skill_set_checks.first()
        self.assertEqual(first.skill_set.pk, skill_set.pk)
        self.assertEqual(
            {obj.pk for obj in first.failed_required_skills.all()},
            {skill_1.pk, skill_2.pk},
        )

    def test_does_not_require_doctrine_definition(self):
        skill_set = SkillSet.objects.create(name="Ship 1")
        skill_1 = SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_1, required_level=5
        )
        skill_2 = SkillSetSkill.objects.create(
            skill_set=skill_set, eve_type=self.skill_type_2, required_level=3
        )

        self.character.update_skill_sets()

        self.assertEqual(self.character.skill_set_checks.count(), 1)
        first = self.character.skill_set_checks.first()
        self.assertEqual(first.skill_set.pk, skill_set.pk)
        self.assertEqual(
            {obj.pk for obj in first.failed_required_skills.all()},
            {skill_1.pk, skill_2.pk},
        )


class TestCharacterWalletJournalEntry(NoSocketsTestCase):
    def test_match_context_type_id(self):
        self.assertEqual(
            CharacterWalletJournalEntry.match_context_type_id("character_id"),
            CharacterWalletJournalEntry.CONTEXT_ID_TYPE_CHARACTER_ID,
        )
        self.assertEqual(
            CharacterWalletJournalEntry.match_context_type_id("contract_id"),
            CharacterWalletJournalEntry.CONTEXT_ID_TYPE_CONTRACT_ID,
        )
        self.assertEqual(
            CharacterWalletJournalEntry.match_context_type_id(None),
            CharacterWalletJournalEntry.CONTEXT_ID_TYPE_UNDEFINED,
        )
