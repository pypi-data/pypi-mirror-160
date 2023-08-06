import datetime as dt

from django.test import TestCase
from django.utils.timezone import now

from allianceauth.eveonline.models import EveAllianceInfo
from allianceauth.tests.auth_utils import AuthUtils

from ...models import Character, CharacterUpdateStatus
from ..testdata.load_entities import load_entities
from ..utils import add_memberaudit_character_to_user, create_memberaudit_character


class TestCharacterManager(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        cls.character_1001 = create_memberaudit_character(1001)
        cls.character_1002 = create_memberaudit_character(1002)

    def test_should_return_set_of_eve_character_ids(self):
        self.assertSetEqual(Character.objects.all().eve_character_ids(), {1001, 1002})


class TestCharacterManagerUserHasAccess(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        # main character with alts
        cls.character_1001 = create_memberaudit_character(1001)  # main
        cls.character_1110 = add_memberaudit_character_to_user(  # alt
            cls.character_1001.character_ownership.user, 1110
        )
        cls.character_1121 = add_memberaudit_character_to_user(  # alt
            cls.character_1001.character_ownership.user, 1121
        )
        # main character with alts
        cls.character_1002 = create_memberaudit_character(1002)
        cls.character_1002.is_shared = True
        cls.character_1002.save()
        AuthUtils.add_permission_to_user_by_name(
            "memberaudit.share_characters",
            cls.character_1002.character_ownership.user,
        )
        cls.character_1103 = add_memberaudit_character_to_user(
            cls.character_1002.character_ownership.user, 1103
        )
        # main characters
        cls.character_1003 = create_memberaudit_character(1003)
        cls.character_1101 = create_memberaudit_character(1101)
        cls.character_1102 = create_memberaudit_character(1102)
        cls.character_1102.is_shared = True
        cls.character_1102.save()
        AuthUtils.add_permission_to_user_by_name(
            "memberaudit.share_characters",
            cls.character_1102.character_ownership.user,
        )
        cls.character_1111 = create_memberaudit_character(1111)
        cls.character_1122 = create_memberaudit_character(1122)
        cls.member_state = AuthUtils.get_member_state()
        cls.member_state.member_alliances.add(
            EveAllianceInfo.objects.get(alliance_id=3001)
        )

    def test_user_owning_character_has_access(self):
        """
        when user is the owner of characters
        then include those characters only
        """
        result_qs = Character.objects.user_has_access(
            user=self.character_1001.character_ownership.user
        )
        self.assertSetEqual(result_qs.eve_character_ids(), {1001, 1110, 1121})

    def test_view_own_corporation_1(self):
        """
        when user has permission to view own corporation and not characters_access
        then include own characters only
        """
        user = self.character_1001.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_same_corporation", user
        )
        result_qs = Character.objects.user_has_access(user=user)
        self.assertSetEqual(result_qs.eve_character_ids(), {1001, 1110, 1121})

    def test_view_own_corporation_2(self):
        """
        when user has permission to view own corporation and characters_access
        then include characters of corporations members (mains + alts)
        """
        user = self.character_1001.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_same_corporation", user
        )
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.characters_access", user
        )
        result_qs = Character.objects.user_has_access(user=user)
        self.assertSetEqual(
            result_qs.eve_character_ids(), {1001, 1110, 1121, 1002, 1103}
        )

    def test_view_own_alliance_1a(self):
        """
        when user has permission to view own alliance and not characters_access
        then include own character only
        """
        user = self.character_1001.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_same_alliance", user
        )
        result_qs = Character.objects.user_has_access(user=user)
        self.assertSetEqual(result_qs.eve_character_ids(), {1001, 1110, 1121})

    def test_view_own_alliance_1b(self):
        """
        when user has permission to view own alliance and characters_access
        then include characters of alliance members (mains + alts)
        """
        user = self.character_1001.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_same_alliance", user
        )
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.characters_access", user
        )
        result_qs = Character.objects.user_has_access(user=user)
        self.assertSetEqual(
            result_qs.eve_character_ids(), {1001, 1110, 1121, 1002, 1003, 1103}
        )

    def test_view_own_alliance_2(self):
        """
        when user has permission to view own alliance and characters_access
        and does not belong to any alliance
        then do not include any alliance characters
        """
        user = self.character_1102.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_same_alliance", user
        )
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.characters_access", user
        )
        result_qs = Character.objects.user_has_access(user=user)
        self.assertSetEqual(result_qs.eve_character_ids(), {1102})

    def test_view_everything_1(self):
        """
        when user has permission to view everything and no characters_access
        then include own character only
        """
        user = self.character_1001.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_everything", user
        )
        result_qs = Character.objects.user_has_access(user=user)
        self.assertSetEqual(result_qs.eve_character_ids(), {1001, 1110, 1121})

    def test_view_everything_2(self):
        """
        when user has permission to view everything and characters_access
        then include all characters
        """
        user = self.character_1001.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_everything", user
        )
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.characters_access", user
        )
        result_qs = Character.objects.user_has_access(user=user)
        self.assertSetEqual(
            result_qs.eve_character_ids(),
            {1001, 1002, 1003, 1101, 1102, 1103, 1110, 1111, 1121, 1122},
        )

    def test_recruiter_access(self):
        """
        when user has recruiter permission
        then include own character plus shared characters from members
        """
        user = self.character_1001.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_shared_characters", user
        )
        result_qs = Character.objects.user_has_access(user=user)
        self.assertSetEqual(
            result_qs.eve_character_ids(), {1001, 1002, 1102, 1110, 1121}
        )

    def test_recruiter_should_loose_access_once_recruit_becomes_member(self):
        # given
        character_1107 = create_memberaudit_character(1107)
        character_1107.is_shared = True
        character_1107.save()
        user = self.character_1001.character_ownership.user
        user = AuthUtils.add_permission_to_user_by_name(
            "memberaudit.view_shared_characters", user
        )
        # when
        result_qs = Character.objects.user_has_access(user=user)
        self.assertNotIn(1107, result_qs.eve_character_ids())


class TestCharacterUpdateStatusManager(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        cls.character_1001 = create_memberaudit_character(1001)

    def test_calculate_stats_1(self):
        """Can handle no data"""
        try:
            CharacterUpdateStatus.objects.statistics()
        except Exception as ex:
            self.fail(f"Unexpected exception {ex} occurred")

    def test_calculate_stats_2(self):
        """normal calculation"""
        my_now = now()
        root_task_id = "1"
        CharacterUpdateStatus.objects.create(
            character=self.character_1001,
            section=Character.UpdateSection.CONTACTS,
            is_success=True,
            started_at=my_now - dt.timedelta(seconds=30),
            finished_at=my_now,
            root_task_id=root_task_id,
        )
        CharacterUpdateStatus.objects.create(
            character=self.character_1001,
            section=Character.UpdateSection.SKILLS,
            is_success=True,
            started_at=my_now + dt.timedelta(seconds=10),
            finished_at=my_now + dt.timedelta(seconds=30),
            root_task_id=root_task_id,
        )
        CharacterUpdateStatus.objects.create(
            character=self.character_1001,
            section=Character.UpdateSection.ASSETS,
            is_success=True,
            started_at=my_now,
            finished_at=my_now + dt.timedelta(seconds=90),
            root_task_id=root_task_id,
        )
        stats = CharacterUpdateStatus.objects.statistics()["update_statistics"]

        # round duration is calculated as total duration
        # from start of first to end of last section
        self.assertEqual(stats["ring_2"]["total"]["duration"], 60)
        self.assertEqual(stats["ring_2"]["total"]["root_task_id"], root_task_id)

        # can identify longest section with character
        self.assertEqual(stats["ring_2"]["first"]["section"], "contacts")
        self.assertEqual(stats["ring_2"]["last"]["section"], "skills")
        self.assertEqual(stats["ring_3"]["max"]["section"], "assets")
        self.assertEqual(stats["ring_3"]["max"]["duration"], 90)
