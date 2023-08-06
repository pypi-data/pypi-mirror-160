import datetime as dt
from typing import Iterable, Tuple

from bravado.exception import HTTPForbidden, HTTPUnauthorized

from django.contrib.auth.models import Group, User
from django.db import models, transaction
from django.db.models import Q
from django.utils.timezone import now
from esi.models import Token
from eveuniverse.models import EveEntity, EveSolarSystem, EveType

from allianceauth.notifications import notify
from allianceauth.services.hooks import get_extension_logger
from app_utils.esi import fetch_esi_status
from app_utils.logging import LoggerAddTag

from .. import __title__
from ..app_settings import (
    MEMBERAUDIT_BULK_METHODS_BATCH_SIZE,
    MEMBERAUDIT_LOCATION_STALE_HOURS,
)
from ..constants import DATETIME_FORMAT, EveCategoryId, EveTypeId
from ..core.fittings import Fitting
from ..helpers import filter_groups_available_to_user
from ..providers import esi

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


class ComplianceGroupDesignationManager(models.Manager):
    def groups(self) -> models.QuerySet:
        """Groups which are compliance groups."""
        return Group.objects.filter(compliancegroupdesignation__isnull=False)

    def update_user(self, user: User):
        """Update compliance groups for user."""
        from ..models import General

        was_compliant = user.groups.filter(
            compliancegroupdesignation__isnull=False
        ).exists()
        is_compliant = General.compliant_users().filter(pk=user.pk).exists()
        if is_compliant:
            # adding groups one by one due to Auth issue #1268
            # TODO: Refactor once issue is fixed
            groups_qs = filter_groups_available_to_user(self.groups(), user).exclude(
                user=user
            )
            for group in groups_qs:
                user.groups.add(group)
            if groups_qs.exists() and not was_compliant:
                logger.info("%s: User is now compliant", user)
                message = (
                    f"Thank you for registering all your characters to {__title__}. "
                    "You now have gained access to additional services."
                )
                notify(
                    user,
                    title=f"{__title__}: All characters registered",
                    message=message,
                    level="success",
                )
        else:
            # removing groups one by one due to Auth issue #1268
            # TODO: Refactor once issue is fixed
            current_groups_qs = self.filter(group__user=user).values_list(
                "group", flat=True
            )
            for group in current_groups_qs:
                user.groups.remove(group)
            if was_compliant:
                logger.info("%s: User is no longer compliant", user)
                message = (
                    f"Some of your characters are not registered to {__title__} "
                    "and you have therefore lost access to services. "
                    "Please add missing characters to restore access."
                )
                notify(
                    user,
                    title=f"{__title__}: Characters not registered",
                    message=message,
                    level="warning",
                )


class EveShipTypeManger(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("eve_group")
            .filter(published=True)
            .filter(eve_group__eve_category_id=EveCategoryId.SHIP)
        )


class EveSkillTypeManger(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(published=True)
            .filter(eve_group__eve_category_id=EveCategoryId.SKILL)
        )


class LocationManager(models.Manager):
    """Manager for Location model

    We recommend preferring the "async" variants, because it includes protection
    against exceeding the ESI error limit due to characters no longer having access
    to structures within their assets, contracts, etc.

    The async methods will first create an empty location and then try to
    update that empty location asynchronously from ESI.
    Updates might be delayed if the error limit is reached.

    The async method can also be used safely in mass updates, where the same
    unauthorized update might be requested multiple times.
    Additional requests for the same location will be ignored within a grace period.
    """

    _UPDATE_EMPTY_GRACE_MINUTES = 5

    def get_or_create_esi(self, id: int, token: Token) -> Tuple[models.Model, bool]:
        """gets or creates location object with data fetched from ESI

        Stale locations will always be updated.
        Empty locations will always be updated after grace period as passed
        """
        return self._get_or_create_esi(id=id, token=token, update_async=False)

    def get_or_create_esi_async(
        self, id: int, token: Token
    ) -> Tuple[models.Model, bool]:
        """gets or creates location object with data fetched from ESI asynchronous"""
        return self._get_or_create_esi(id=id, token=token, update_async=True)

    def _get_or_create_esi(
        self, id: int, token: Token, update_async: bool = True
    ) -> Tuple[models.Model, bool]:
        id = int(id)
        empty_threshold = now() - dt.timedelta(minutes=self._UPDATE_EMPTY_GRACE_MINUTES)
        stale_threshold = now() - dt.timedelta(hours=MEMBERAUDIT_LOCATION_STALE_HOURS)
        try:
            location = self.exclude(
                (Q(eve_type__isnull=True) & Q(updated_at__lt=empty_threshold))
                | Q(updated_at__lt=stale_threshold)
            ).get(id=id)
            created = False
            return location, created
        except self.model.DoesNotExist:
            if update_async:
                return self.update_or_create_esi_async(id=id, token=token)
            return self.update_or_create_esi(id=id, token=token)

    def update_or_create_esi_async(
        self, id: int, token: Token
    ) -> Tuple[models.Model, bool]:
        """updates or creates location object with data fetched from ESI asynchronous"""
        return self._update_or_create_esi(id=id, token=token, update_async=True)

    def update_or_create_esi(self, id: int, token: Token) -> Tuple[models.Model, bool]:
        """updates or creates location object with data fetched from ESI synchronous

        The preferred method to use is: `update_or_create_esi_async()`,
        since it protects against exceeding the ESI error limit and which can happen
        a lot due to users not having authorization to access a structure.
        """
        return self._update_or_create_esi(id=id, token=token, update_async=False)

    def _update_or_create_esi(
        self, id: int, token: Token, update_async: bool = True
    ) -> Tuple[models.Model, bool]:
        id = int(id)
        if self.model.is_asset_safety_id(id):
            eve_type, _ = EveType.objects.get_or_create_esi(
                id=EveTypeId.ASSET_SAFETY_WRAP
            )
            return self.update_or_create(
                id=id,
                defaults={"name": "ASSET SAFETY", "eve_type": eve_type},
            )
        elif self.model.is_solar_system_id(id):
            eve_solar_system, _ = EveSolarSystem.objects.get_or_create_esi(id=id)
            eve_type, _ = EveType.objects.get_or_create_esi(id=EveTypeId.SOLAR_SYSTEM)
            return self.update_or_create(
                id=id,
                defaults={
                    "name": eve_solar_system.name,
                    "eve_solar_system": eve_solar_system,
                    "eve_type": eve_type,
                },
            )
        elif self.model.is_station_id(id):
            logger.info("%s: Fetching station from ESI", id)
            station = esi.client.Universe.get_universe_stations_station_id(
                station_id=id
            ).results()
            return self._station_update_or_create_dict(id=id, station=station)
        elif self.model.is_structure_id(id):
            if update_async:
                return self._structure_update_or_create_esi_async(id=id, token=token)
            return self.structure_update_or_create_esi(id=id, token=token)
        logger.warning(
            "%s: Creating empty location for ID not matching any known pattern:", id
        )
        return self.get_or_create(id=id)

    def _station_update_or_create_dict(
        self, id: int, station: dict
    ) -> Tuple[models.Model, bool]:
        if station.get("system_id"):
            eve_solar_system, _ = EveSolarSystem.objects.get_or_create_esi(
                id=station.get("system_id")
            )
        else:
            eve_solar_system = None

        if station.get("type_id"):
            eve_type, _ = EveType.objects.get_or_create_esi(id=station.get("type_id"))
        else:
            eve_type = None

        if station.get("owner"):
            owner, _ = EveEntity.objects.get_or_create_esi(id=station.get("owner"))
        else:
            owner = None

        return self.update_or_create(
            id=id,
            defaults={
                "name": station.get("name", ""),
                "eve_solar_system": eve_solar_system,
                "eve_type": eve_type,
                "owner": owner,
            },
        )

    def _structure_update_or_create_esi_async(self, id: int, token: Token):
        from ..tasks import DEFAULT_TASK_PRIORITY
        from ..tasks import update_structure_esi as task_update_structure_esi

        id = int(id)
        location, created = self.get_or_create(id=id)
        task_update_structure_esi.apply_async(
            kwargs={"id": id, "token_pk": token.pk},
            priority=DEFAULT_TASK_PRIORITY,
        )
        return location, created

    def structure_update_or_create_esi(self, id: int, token: Token):
        """Update or creates structure from ESI"""
        fetch_esi_status().raise_for_status()
        try:
            structure = esi.client.Universe.get_universe_structures_structure_id(
                structure_id=id, token=token.valid_access_token()
            ).results()
        except (HTTPUnauthorized, HTTPForbidden) as http_error:
            logger.warn(
                "%s: No access to structure #%s: %s",
                token.character_name,
                id,
                http_error,
            )
            return self.get_or_create(id=id)
        else:
            return self._structure_update_or_create_dict(id=id, structure=structure)

    def _structure_update_or_create_dict(
        self, id: int, structure: dict
    ) -> Tuple[models.Model, bool]:
        """creates a new Location object from a structure dict"""
        if structure.get("solar_system_id"):
            eve_solar_system, _ = EveSolarSystem.objects.get_or_create_esi(
                id=structure.get("solar_system_id")
            )
        else:
            eve_solar_system = None

        if structure.get("type_id"):
            eve_type, _ = EveType.objects.get_or_create_esi(id=structure.get("type_id"))
        else:
            eve_type = None

        if structure.get("owner_id"):
            owner, _ = EveEntity.objects.get_or_create_esi(id=structure.get("owner_id"))
        else:
            owner = None

        return self.update_or_create(
            id=id,
            defaults={
                "name": structure.get("name", ""),
                "eve_solar_system": eve_solar_system,
                "eve_type": eve_type,
                "owner": owner,
            },
        )


class MailEntityManager(models.Manager):
    def get_or_create_esi(
        self, id: int, category: str = None
    ) -> Tuple[models.Model, bool]:
        return self._get_or_create_esi(id=id, category=category, update_async=False)

    def get_or_create_esi_async(
        self, id: int, category: str = None
    ) -> Tuple[models.Model, bool]:
        return self._get_or_create_esi(id=id, category=category, update_async=True)

    def _get_or_create_esi(
        self, id: int, category: str, update_async: bool
    ) -> Tuple[models.Model, bool]:
        id = int(id)
        try:
            return self.get(id=id), False
        except self.model.DoesNotExist:
            if update_async:
                return self.update_or_create_esi_async(id=id, category=category)
            return self.update_or_create_esi(id=id, category=category)

    def update_or_create_esi(
        self, id: int, category: str = None
    ) -> Tuple[models.Model, bool]:
        """will try to update or create a new object from ESI

        Mailing lists can not be resolved from ESI
        and will therefore be created without name

        Trying to resolve a mailing list from ESI will result in an ESI error,
        which is masked by this method.

        Exceptions:
        - EsiOffline: ESI offline
        - EsiErrorLimitExceeded: ESI error limit exceeded
        - HTTP errors
        """
        id = int(id)
        try:
            obj = self.get(id=id)
            category = obj.category
        except self.model.DoesNotExist:
            pass

        if not category or category == self.model.Category.UNKNOWN:
            fetch_esi_status().raise_for_status()
            eve_entity, _ = EveEntity.objects.get_or_create_esi(id=id)
            if eve_entity:
                return self.update_or_create_from_eve_entity(eve_entity)
            return self.update_or_create(
                id=id,
                defaults={"category": self.model.Category.MAILING_LIST},
            )
        else:
            if category == self.model.Category.MAILING_LIST:
                return self.update_or_create(
                    id=id,
                    defaults={"category": self.model.Category.MAILING_LIST},
                )
            return self.update_or_create_from_eve_entity_id(id=id)

    def update_or_create_esi_async(
        self, id: int, category: str = None
    ) -> Tuple[models.Model, bool]:
        """Same as update_or_create_esi, but will create and return an empty object and delegate the ID resolution to a task (if needed),
        which will automatically retry on many common error conditions
        """
        id = int(id)
        try:
            obj = self.get(id=id)
            if obj.category == self.model.Category.MAILING_LIST:
                return obj, False
            else:
                category = obj.category

        except self.model.DoesNotExist:
            pass

        if category and category in self.model.Category.eve_entity_compatible():
            return self.update_or_create_esi(id=id, category=category)
        return self._update_or_create_esi_async(id=id)

    def _update_or_create_esi_async(self, id: int) -> Tuple[models.Model, bool]:
        from ..tasks import DEFAULT_TASK_PRIORITY
        from ..tasks import update_mail_entity_esi as task_update_mail_entity_esi

        id = int(id)
        obj, created = self.get_or_create(
            id=id, defaults={"category": self.model.Category.UNKNOWN}
        )
        task_update_mail_entity_esi.apply_async(
            kwargs={"id": id}, priority=DEFAULT_TASK_PRIORITY
        )
        return obj, created

    def update_or_create_from_eve_entity(
        self, eve_entity: EveEntity
    ) -> Tuple[models.Model, bool]:
        category_map = {
            EveEntity.CATEGORY_ALLIANCE: self.model.Category.ALLIANCE,
            EveEntity.CATEGORY_CHARACTER: self.model.Category.CHARACTER,
            EveEntity.CATEGORY_CORPORATION: self.model.Category.CORPORATION,
        }
        return self.update_or_create(
            id=eve_entity.id,
            defaults={
                "category": category_map[eve_entity.category],
                "name": eve_entity.name,
            },
        )

    def update_or_create_from_eve_entity_id(self, id: int) -> Tuple[models.Model, bool]:
        eve_entity, _ = EveEntity.objects.get_or_create_esi(id=int(id))
        return self.update_or_create_from_eve_entity(eve_entity)

    def bulk_update_names(
        self, objs: Iterable[models.Model], keep_names: bool = False
    ) -> None:
        """Update names for given objects with categories
        that can be resolved by EveEntity (e.g. Character)

        Args:
        - obj: Existing objects to be updated
        - keep_names: When True objects that already have a name will not be updated

        """
        valid_categories = self.model.Category.eve_entity_compatible()
        valid_objs = {
            obj.id: obj
            for obj in objs
            if obj.category in valid_categories and (not keep_names or not obj.name)
        }
        if valid_objs:
            resolver = EveEntity.objects.bulk_resolve_names(valid_objs.keys())
            for obj in valid_objs.values():
                obj.name = resolver.to_name(obj.id)

            self.bulk_update(
                valid_objs.values(),
                ["name"],
                batch_size=MEMBERAUDIT_BULK_METHODS_BATCH_SIZE,
            )

    # @transaction.atomic()
    def update_for_character(self, character, mailing_lists):
        logger.info(
            "%s: Updating %s mailing lists", character, set(mailing_lists.keys())
        )
        new_mailing_lists = list()
        for list_id, mailing_list in mailing_lists.items():
            mailing_list_obj, _ = self.model.objects.update_or_create(
                id=list_id,
                defaults={
                    "category": self.model.Category.MAILING_LIST,
                    "name": mailing_list.get("name"),
                },
            )
            new_mailing_lists.append(mailing_list_obj)

        return new_mailing_lists


class SkillSetManager(models.Manager):
    def update_or_create_from_fitting(
        self,
        fitting: Fitting,
        user: User = None,
        skill_set_group=None,
        skill_set_name=None,
    ) -> Tuple[models.Model, bool]:
        from ..models import SkillSetSkill

        required_skills = fitting.required_skills()
        description = (
            f"Generated from EFT fitting '{fitting.name}' "
            f"by {user if user else '?'} "
            f"at {now().strftime(DATETIME_FORMAT)}"
        )
        if not skill_set_name:
            skill_set_name = fitting.name
        with transaction.atomic():
            skill_set, created = self.get_or_create(
                name=str(skill_set_name),
                defaults={
                    "ship_type": fitting.ship_type,
                    "description": description,
                },
            )
            skill_set.skills.all().delete()
            skills = [
                SkillSetSkill(
                    skill_set=skill_set,
                    eve_type=skill.eve_type,
                    required_level=skill.level,
                )
                for skill in required_skills
            ]
            SkillSetSkill.objects.bulk_create(skills)
            if skill_set_group:
                skill_set_group.skill_sets.add(skill_set)

        return skill_set, created

    def compile_groups_map(self) -> dict:
        """Compiles map of all skill sets by groups."""

        def _add_skill_set(groups_map, skill_set, group=None):
            group_id = group.id if group else 0
            if group_id not in groups_map.keys():
                groups_map[group_id] = {"group": group, "skill_sets": []}
            groups_map[group_id]["skill_sets"].append(skill_set)

        groups_map = dict()
        for skill_set in (
            self.select_related("ship_type").prefetch_related("groups").all()
        ):
            if skill_set.groups.exists():
                for group in skill_set.groups.all():
                    _add_skill_set(groups_map, skill_set, group)
            else:
                _add_skill_set(groups_map, skill_set, group=None)
        return groups_map
