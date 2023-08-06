import datetime as dt
from typing import Optional

import humanize

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy
from eveuniverse.core import eveimageserver
from eveuniverse.models import EveType

from allianceauth.services.hooks import get_extension_logger
from app_utils.logging import LoggerAddTag
from app_utils.views import (
    bootstrap_icon_plus_name_html,
    bootstrap_label_html,
    link_html,
    no_wrap_html,
    yesno_str,
)

from .. import __title__
from ..constants import (
    DATETIME_FORMAT,
    DEFAULT_ICON_SIZE,
    MAIL_LABEL_ID_ALL_MAILS,
    MAP_ARABIC_TO_ROMAN_NUMBERS,
    MY_DATETIME_FORMAT,
    SKILL_SET_DEFAULT_ICON_TYPE_ID,
    EveDogmaAttributeId,
)
from ..decorators import fetch_character_if_allowed
from ..models import Character, CharacterMail, SkillSet, SkillSetSkill
from ._common import UNGROUPED_SKILL_SET, eve_solar_system_to_html

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

ICON_SIZE_64 = 64
CHARACTER_VIEWER_DEFAULT_TAB = "mails"

ICON_FAILED = "fas fa-times boolean-icon-false"
ICON_PARTIAL = "fas fa-check text-warning"
ICON_FULL = "fas fa-check-double text-success"
ICON_MET_ALL_REQUIRED = "fas fa-check text-success"


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_jump_clones_data(
    request, character_pk: int, character: Character
) -> HttpResponse:
    data = list()
    try:
        for jump_clone in (
            character.jump_clones.select_related(
                "location",
                "location__eve_solar_system",
                "location__eve_solar_system__eve_constellation__eve_region",
            )
            .prefetch_related("implants", "implants__eve_type__dogma_attributes")
            .all()
        ):
            if not jump_clone.location.is_empty:
                eve_solar_system = jump_clone.location.eve_solar_system
                solar_system = eve_solar_system_to_html(
                    eve_solar_system, show_region=False
                )
                region = eve_solar_system.eve_constellation.eve_region.name
            else:
                solar_system = "-"
                region = "-"

            implants_data = list()
            for implant in jump_clone.implants.all():
                dogma_attributes = {
                    obj.eve_dogma_attribute_id: obj.value
                    for obj in implant.eve_type.dogma_attributes.all()
                }
                try:
                    slot_num = int(dogma_attributes[EveDogmaAttributeId.IMPLANT_SLOT])
                except KeyError:
                    slot_num = 0
                implants_data.append(
                    {
                        "name": implant.eve_type.name,
                        "icon_url": implant.eve_type.icon_url(
                            DEFAULT_ICON_SIZE, variant=EveType.IconVariant.REGULAR
                        ),
                        "slot_num": slot_num,
                    }
                )
            if implants_data:
                implants = "<br>".join(
                    bootstrap_icon_plus_name_html(
                        x["icon_url"], no_wrap_html(x["name"]), size=24
                    )
                    for x in sorted(implants_data, key=lambda k: k["slot_num"])
                )
            else:
                implants = "(none)"

            data.append(
                {
                    "id": jump_clone.pk,
                    "region": region,
                    "solar_system": solar_system,
                    "location": jump_clone.location.name_plus,
                    "implants": implants,
                }
            )
    except ObjectDoesNotExist:
        pass

    return JsonResponse({"data": data})


def _character_mail_headers_data(request, character, mail_headers_qs) -> JsonResponse:
    mails_data = list()
    try:
        for mail in mail_headers_qs.select_related("sender").prefetch_related(
            "recipients"
        ):
            mail_ajax_url = reverse(
                "memberaudit:character_mail", args=[character.pk, mail.pk]
            )
            if mail.body:
                actions_html = (
                    '<button type="button" class="btn btn-primary" '
                    'data-toggle="modal" data-target="#modalCharacterMail" '
                    f"data-ajax_url={mail_ajax_url}>"
                    '<i class="fas fa-search"></i></button>'
                )
            else:
                actions_html = ""

            mails_data.append(
                {
                    "mail_id": mail.mail_id,
                    "from": mail.sender.name_plus,
                    "to": ", ".join(
                        sorted([obj.name_plus for obj in mail.recipients.all()])
                    ),
                    "subject": mail.subject,
                    "sent": mail.timestamp.isoformat(),
                    "action": actions_html,
                    "is_read": mail.is_read,
                    "is_unread_str": yesno_str(mail.is_read is False),
                }
            )
    except ObjectDoesNotExist:
        pass

    return JsonResponse({"data": mails_data})


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_mail_headers_by_label_data(
    request, character_pk: int, character: Character, label_id: int
) -> JsonResponse:
    if label_id == MAIL_LABEL_ID_ALL_MAILS:
        mail_headers_qs = character.mails.all()
    else:
        mail_headers_qs = character.mails.filter(labels__label_id=label_id)

    return _character_mail_headers_data(request, character, mail_headers_qs)


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_mail_headers_by_list_data(
    request, character_pk: int, character: Character, list_id: int
) -> JsonResponse:
    mail_headers_qs = character.mails.filter(recipients__id=list_id)
    return _character_mail_headers_data(request, character, mail_headers_qs)


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_mail(
    request, character_pk: int, character: Character, mail_pk: int
) -> JsonResponse:
    try:
        mail = (
            character.mails.select_related("sender")
            .prefetch_related("recipients")
            .get(pk=mail_pk)
        )
    except CharacterMail.DoesNotExist:
        error_msg = f"Mail with pk {mail_pk} not found for character {character}"
        logger.warning(error_msg)
        return HttpResponseNotFound(error_msg)
    recipients = sorted(
        [
            {
                "name": obj.name_plus,
                "link": link_html(obj.external_url(), obj.name_plus),
            }
            for obj in mail.recipients.all()
        ],
        key=lambda k: k["name"],
    )
    context = {
        "mail_id": mail.mail_id,
        "labels": list(mail.labels.values_list("label_id", flat=True)),
        "sender": link_html(mail.sender.external_url(), mail.sender.name_plus),
        "recipients": format_html(", ".join([obj["link"] for obj in recipients])),
        "subject": mail.subject,
        "timestamp": mail.timestamp,
        "body": mail.body_html if mail.body else None,
        "MY_DATETIME_FORMAT": MY_DATETIME_FORMAT,
    }
    return render(
        request, "memberaudit/modals/character_viewer/mail_content.html", context
    )


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_skillqueue_data(
    request, character_pk: int, character: Character
) -> JsonResponse:
    data = list()
    try:
        for row in character.skillqueue.select_related("eve_type").filter(
            character_id=character_pk
        ):
            level_roman = MAP_ARABIC_TO_ROMAN_NUMBERS[row.finished_level]
            skill_str = f"{row.eve_type.name}&nbsp;{level_roman}"
            if row.is_active:
                skill_str += " [ACTIVE]"

            if row.finish_date:
                finish_date_humanized = humanize.naturaltime(
                    dt.datetime.now()
                    + dt.timedelta(
                        seconds=(
                            row.finish_date.timestamp() - dt.datetime.now().timestamp()
                        )
                    )
                )
                finish_date_str = (
                    f"{row.finish_date.strftime(DATETIME_FORMAT)} "
                    f"({finish_date_humanized})"
                )
                finish_date_sort = row.finish_date.isoformat()
            else:
                finish_date_str = gettext("(training not active)")
                finish_date_sort = None

            data.append(
                {
                    "position": row.queue_position + 1,
                    "skill": skill_str,
                    "finished": {
                        "display": finish_date_str,
                        "sort": finish_date_sort,
                    },
                    "is_active": row.is_active,
                }
            )
    except ObjectDoesNotExist:
        pass

    return JsonResponse({"data": data})


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_skill_sets_data(
    request, character_pk: int, character: Character
) -> JsonResponse:
    def _create_row(skill_check):
        def _skill_set_name_html(skill_set):
            url = (
                skill_set.ship_type.icon_url(
                    DEFAULT_ICON_SIZE, variant=EveType.IconVariant.REGULAR
                )
                if skill_set.ship_type
                else eveimageserver.type_icon_url(
                    SKILL_SET_DEFAULT_ICON_TYPE_ID, size=DEFAULT_ICON_SIZE
                )
            )
            ship_icon = f'<img width="24" heigh="24" src="{url}"/>'
            return ship_icon + "&nbsp;&nbsp;" + skill_set.name

        def _group_name(group):
            if group:
                return (
                    group.name_plus if group.is_active else group.name + " [Not active]"
                )
            return UNGROUPED_SKILL_SET

        def _compile_failed_skills(skill_set_skills, level_name) -> Optional[list]:
            skills2 = sorted(
                [
                    {
                        "name": obj.eve_type.name,
                        "required_level": obj.required_level,
                        "recommended_level": obj.recommended_level,
                    }
                    for obj in skill_set_skills
                ],
                key=lambda k: k["name"].lower(),
            )
            return [
                bootstrap_label_html(
                    format_html(
                        "{}&nbsp;{}",
                        obj["name"],
                        MAP_ARABIC_TO_ROMAN_NUMBERS[obj[level_name]],
                    ),
                    "default",
                )
                for obj in skills2
            ]

        def _format_failed_skills(skills) -> str:
            return " ".join(skills) if skills else "-"

        failed_required_skills = list(skill_check.failed_required_skills_prefetched)
        has_required = not bool(failed_required_skills)
        failed_required_skills_str = _format_failed_skills(
            _compile_failed_skills(failed_required_skills, "required_level")
        )
        failed_recommended_skills = list(
            skill_check.failed_recommended_skills_prefetched
        )
        has_recommended = not bool(failed_recommended_skills)
        failed_recommended_skills_str = _format_failed_skills(
            _compile_failed_skills(failed_recommended_skills, "recommended_level")
        )
        is_doctrine = group.is_doctrine if group else False
        ajax_children_url = reverse(
            "memberaudit:character_skill_set_details",
            args=[character.pk, skill_check.skill_set_id],
        )
        actions_html = (
            '<button type="button" class="btn btn-primary" '
            'data-toggle="modal" data-target="#modalCharacterSkillSetDetails" '
            f"data-ajax_skill_set_detail={ ajax_children_url }>"
            '<i class="fas fa-search"></i></button>'
        )
        return {
            "id": skill_check.id,
            "group": _group_name(group),
            "skill_set": _skill_set_name_html(skill_check.skill_set),
            "skill_set_name": skill_set.name,
            "is_doctrine_str": yesno_str(is_doctrine),
            "failed_required_skills": failed_required_skills_str,
            "has_required": has_required,
            "has_required_str": yesno_str(has_required),
            "failed_recommended_skills": failed_recommended_skills_str,
            "has_recommended": has_recommended,
            "has_recommended_str": yesno_str(has_recommended),
            "action": actions_html,
        }

    groups_map = SkillSet.objects.compile_groups_map()
    skill_checks_qs = (
        character.skill_set_checks.select_related("skill_set", "skill_set__ship_type")
        .prefetch_related(
            Prefetch(
                "failed_required_skills",
                queryset=SkillSetSkill.objects.select_related("eve_type"),
                to_attr="failed_required_skills_prefetched",
            )
        )
        .prefetch_related(
            Prefetch(
                "failed_recommended_skills",
                queryset=SkillSetSkill.objects.select_related("eve_type"),
                to_attr="failed_recommended_skills_prefetched",
            )
        )
        .all()
    )
    skill_checks = {obj.skill_set_id: obj for obj in skill_checks_qs}
    data = []
    for group_map in groups_map.values():
        group = group_map["group"]
        for skill_set in group_map["skill_sets"]:
            try:
                skill_check = skill_checks[skill_set.id]
            except KeyError:
                continue
            else:
                row = _create_row(skill_check)
                data.append(row)
    data = sorted(data, key=lambda k: (k["group"].lower(), k["skill_set_name"].lower()))
    return JsonResponse({"data": data})


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_skill_set_details(
    request, character_pk: int, character: Character, skill_set_pk: int
) -> HttpResponse:

    skill_set = get_object_or_404(SkillSet, pk=skill_set_pk)
    skill_set_skills_qs = SkillSetSkill.objects.select_related("eve_type").filter(
        skill_set_id=skill_set_pk
    )
    skill_set_skills = {obj.eve_type_id: obj for obj in skill_set_skills_qs}
    character_skills_qs = character.skills.select_related("eve_type").filter(
        eve_type_id__in=skill_set_skills.keys()
    )
    character_skills = {obj.eve_type_id: obj for obj in character_skills_qs}
    out_data = list()
    url = (
        skill_set.ship_type.icon_url(ICON_SIZE_64, variant=EveType.IconVariant.REGULAR)
        if skill_set.ship_type
        else eveimageserver.type_icon_url(
            SKILL_SET_DEFAULT_ICON_TYPE_ID, size=ICON_SIZE_64
        )
    )
    missing_skills = []
    for skill_id, skill in skill_set_skills.items():
        character_skill = character_skills.get(skill_id)
        recommended_level_str = "-"
        required_level_str = "-"
        current_str = "-"
        result_icon = ICON_FAILED
        met_required = True

        if character_skill:
            current_str = MAP_ARABIC_TO_ROMAN_NUMBERS[
                character_skill.active_skill_level
            ]

        if skill.recommended_level:
            recommended_level_str = MAP_ARABIC_TO_ROMAN_NUMBERS[skill.recommended_level]

        if skill.required_level:
            required_level_str = MAP_ARABIC_TO_ROMAN_NUMBERS[skill.required_level]

        if not character_skill:
            result_icon = ICON_FAILED
            met_required = False
        else:
            if (
                skill.required_level
                and not skill.recommended_level
                and character_skill.active_skill_level >= skill.required_level
            ):
                result_icon = ICON_FULL
            elif (
                skill.recommended_level
                and character_skill.active_skill_level >= skill.recommended_level
            ):
                result_icon = ICON_FULL
            elif (
                skill.required_level
                and character_skill.active_skill_level >= skill.required_level
            ):
                result_icon = ICON_PARTIAL
            else:
                met_required = False

        if not character_skill or (
            character_skill and character_skill.active_skill_level < skill.maximum_level
        ):
            missing_skills.append(skill.maximum_skill_str)

        out_data.append(
            {
                "name": skill.eve_type.name,
                "required": required_level_str,
                "recommended": recommended_level_str,
                "current": current_str,
                "result_icon": result_icon,
                "met_required": met_required,
            }
        )

    met_all_required = True
    for data in out_data:
        if not data["met_required"]:
            met_all_required = False
            break

    out_data = sorted(out_data, key=lambda k: (k["name"].lower()))
    missing_skills_str = "\n".join(missing_skills) if missing_skills else ""
    context = {
        "name": skill_set.name,
        "description": skill_set.description,
        "ship_url": url,
        "skills": out_data,
        "met_all_required": met_all_required,
        "icon_failed": ICON_FAILED,
        "icon_partial": ICON_PARTIAL,
        "icon_full": ICON_FULL,
        "icon_met_all_required": ICON_MET_ALL_REQUIRED,
        "missing_skills_str": missing_skills_str,
    }

    return render(
        request,
        "memberaudit/modals/character_viewer/skill_set_content.html",
        context,
    )


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_skills_data(
    request, character_pk: int, character: Character
) -> JsonResponse:
    skills_data = list()
    try:
        for skill in character.skills.select_related("eve_type", "eve_type__eve_group"):
            level_str = MAP_ARABIC_TO_ROMAN_NUMBERS[skill.active_skill_level]
            skill_name = format_html(
                '<span title="{}">{} {}</span>',
                skill.eve_type.description,
                skill.eve_type.name,
                level_str,
            )
            skills_data.append(
                {
                    "group": skill.eve_type.eve_group.name,
                    "skill": skill.eve_type.name,
                    "skill_name": skill_name,
                    "level": skill.active_skill_level,
                    "level_str": level_str,
                }
            )
    except ObjectDoesNotExist:
        pass

    return JsonResponse({"data": skills_data})


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_wallet_journal_data(
    request, character_pk: int, character: Character
) -> JsonResponse:
    wallet_data = list()
    try:
        for row in character.wallet_journal.select_related(
            "first_party", "second_party"
        ).all():
            first_party = row.first_party.name if row.first_party else "-"
            second_party = row.second_party.name if row.second_party else "-"
            wallet_data.append(
                {
                    "date": row.date.isoformat(),
                    "ref_type": row.ref_type.replace("_", " ").title(),
                    "first_party": first_party,
                    "second_party": second_party,
                    "amount": float(row.amount),
                    "balance": float(row.balance),
                    "description": row.description,
                    "reason": row.reason,
                }
            )
    except ObjectDoesNotExist:
        pass

    return JsonResponse({"data": wallet_data})


@login_required
@permission_required("memberaudit.basic_access")
@fetch_character_if_allowed()
def character_wallet_transactions_data(
    request, character_pk: int, character: Character
) -> JsonResponse:
    wallet_data = list()
    try:
        for row in character.wallet_transactions.select_related(
            "client", "eve_type", "location"
        ).all():
            buy_or_sell = gettext_lazy("Buy") if row.is_buy else gettext_lazy("Sell")
            wallet_data.append(
                {
                    "date": row.date.isoformat(),
                    "quantity": row.quantity,
                    "type": row.eve_type.name,
                    "unit_price": float(row.unit_price),
                    "total": float(
                        row.unit_price * row.quantity * (-1 if row.is_buy else 1)
                    ),
                    "client": row.client.name,
                    "location": row.location.name,
                    "is_buy": row.is_buy,
                    "buy_or_sell": buy_or_sell,
                }
            )
    except ObjectDoesNotExist:
        pass
    return JsonResponse({"data": wallet_data})
