from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import Case, Count, Max, Prefetch, Q, Value, When
from django.forms.models import BaseInlineFormSet
from django.shortcuts import redirect, render
from django.utils.html import format_html
from eveuniverse.models import EveType

from . import tasks
from .constants import EveCategoryId
from .models import (
    Character,
    CharacterUpdateStatus,
    ComplianceGroupDesignation,
    EveShipType,
    EveSkillType,
    Location,
    SkillSet,
    SkillSetGroup,
    SkillSetSkill,
)
from .tasks import add_compliant_users_to_group, clear_users_from_group


class ComplianceGroupDesignationForm(forms.ModelForm):
    class Meta:
        model = ComplianceGroupDesignation
        fields = ("group",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields["group"].queryset = Group.objects.filter(
                authgroup__internal=True, compliancegroupdesignation__isnull=True
            ).order_by("name")
        except KeyError:
            pass


@admin.register(ComplianceGroupDesignation)
class ComplianceGroupDesignationAdmin(admin.ModelAdmin):
    form = ComplianceGroupDesignationForm
    ordering = ("group__name",)
    list_display = ("_group_name", "_states")
    list_display_links = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("group").prefetch_related("group__authgroup__states")

    def save_model(self, request, obj, *args, **kwargs) -> None:
        super().save_model(request, obj, *args, **kwargs)
        add_compliant_users_to_group.delay(obj.group.pk)

    def delete_queryset(self, request, queryset) -> None:
        for obj in queryset:
            clear_users_from_group.delay(obj.group.pk)
            obj.delete()

    @admin.display(ordering="group__name")
    def _group_name(self, obj) -> str:
        return obj.group.name

    @admin.display(description="Restricted to states")
    def _states(self, obj):
        states = [state.name for state in obj.group.authgroup.states.all()]
        return sorted(states) if states else "-"

    def has_change_permission(self, request, obj=None):
        return False


class EveUniverseEntityModelAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    ordering = ["name"]
    search_fields = ["name"]


@admin.register(EveShipType)
class EveShipTypeAdmin(EveUniverseEntityModelAdmin):
    pass


@admin.register(EveSkillType)
class EveSkillTypeAdmin(EveUniverseEntityModelAdmin):
    pass


class SyncStatusAdminInline(admin.TabularInline):
    model = CharacterUpdateStatus
    fields = (
        "section",
        "is_success",
        "last_error_message",
        "started_at",
        "finished_at",
        "root_task_id",
    )
    ordering = ["section"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("authentication/css/admin.css",)}

    list_display = (
        "_character_pic",
        "_character",
        "_main",
        "_state",
        "_organization",
        "created_at",
        "_last_update_at",
        "_last_update_ok",
        "_missing_sections",
    )
    list_display_links = (
        "_character_pic",
        "_character",
    )
    list_filter = (
        "created_at",
        "character_ownership__user__profile__state",
        "character_ownership__user__profile__main_character__alliance_name",
    )
    list_select_related = (
        "character_ownership__user",
        "character_ownership__user__profile__main_character",
        "character_ownership__user__profile__state",
        "character_ownership__character",
    )
    ordering = ["character_ownership__character__character_name"]
    search_fields = [
        "character_ownership__character__character_name",
        "character_ownership__user__profile__main_character__corporation_name",
        "character_ownership__user__profile__main_character__alliance_name",
    ]
    exclude = ("mailing_lists",)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        num_sections_total = len(Character.UpdateSection.choices)
        return (
            qs.prefetch_related("update_status_set")
            .annotate(last_update_at=Max("update_status_set__finished_at"))
            .annotate(
                num_sections_ok=Count(
                    "update_status_set", filter=Q(update_status_set__is_success=True)
                )
            )
            .annotate(
                num_sections_failed=Count(
                    "update_status_set", filter=Q(update_status_set__is_success=False)
                )
            )
            .annotate(
                is_last_update_ok=Case(
                    When(num_sections_failed__gt=0, then=False),
                    When(num_sections_ok=num_sections_total, then=True),
                    default=Value(None),
                )
            )
        )

    def get_actions(self, request):
        """Remove the default delete action from the drop-down."""
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    @admin.display(description="")
    def _character_pic(self, obj):
        character = obj.character_ownership.character
        return format_html(
            '<img src="{}" class="img-circle">', character.portrait_url(size=32)
        )

    @admin.display(ordering="character_ownership__character__character_name")
    def _character(self, obj) -> str:
        return str(obj.character_ownership.character)

    @admin.display(ordering="character_ownership__user__profile__main_character")
    def _main(self, obj) -> str:
        try:
            name = obj.character_ownership.user.profile.main_character.character_name
        except AttributeError:
            return None
        return str(name)

    @admin.display(ordering="character_ownership__user__profile__state__name")
    def _state(self, obj) -> str:
        return str(obj.character_ownership.user.profile.state)

    @admin.display(
        ordering="character_ownership__user__profile__main_character__corporation_name"
    )
    def _organization(self, obj) -> str:
        try:
            main = obj.character_ownership.user.profile.main_character
            return "{}{}".format(
                main.corporation_name,
                f" [{main.alliance_ticker}]" if main.alliance_ticker else "",
            )
        except AttributeError:
            return None

    @admin.display(boolean=True, ordering="is_last_update_ok")
    def _last_update_ok(self, obj):
        return obj.is_last_update_ok

    @admin.display(ordering="last_update_at")
    def _last_update_at(self, obj):
        return obj.last_update_at

    def _missing_sections(self, obj):
        existing = {x.section for x in obj.update_status_set.all()}
        all_sections = set(Character.UpdateSection.values)
        missing = all_sections.difference(existing)
        if missing:
            return sorted(
                [Character.UpdateSection.display_name(obj) for obj in missing]
            )
        return None

    actions = [
        "delete_characters",
        "update_characters",
        "update_assets",
        "update_location",
        "update_online_status",
    ]

    @admin.display(description="Delete selected characters")
    def delete_characters(self, request, queryset):
        if "apply" in request.POST:
            for obj in queryset:
                tasks.delete_character.delay(character_pk=obj.pk)
            self.message_user(
                request,
                f"Started deleting {queryset.count()} character(s). "
                "This can take a minute.",
            )
            return redirect(request.get_full_path())
        return render(
            request,
            "admin/memberaudit/character/confirm_character_deletion.html",
            {
                "title": "Are you sure you want to delete these characters?",
                "queryset": queryset.all(),
            },
        )

    @admin.display(description="Update selected characters from EVE server")
    def update_characters(self, request, queryset):
        for obj in queryset:
            tasks.update_character.delay(character_pk=obj.pk, force_update=True)
            self.message_user(request, f"Started updating character: {obj}. ")

    @admin.display(description="Update assets for selected characters from EVE server")
    def update_assets(self, request, queryset):
        for obj in queryset:
            tasks.update_character_assets.delay(character_pk=obj.pk, force_update=True)
            self.message_user(
                request, f"Started updating assets for character: {obj}. "
            )

    @admin.display(
        description=(
            f"Update {Character.UpdateSection.display_name(Character.UpdateSection.LOCATION)} "
            "for selected characters from EVE server"
        )
    )
    def update_location(self, request, queryset):
        section = Character.UpdateSection.LOCATION
        for obj in queryset:
            tasks.update_character_section.delay(character_pk=obj.pk, section=section)
            self.message_user(
                request,
                f"Started updating {Character.UpdateSection.display_name(section)} for character: {obj}. ",
            )

    @admin.display(
        description=(
            "Update "
            f"{Character.UpdateSection.display_name(Character.UpdateSection.ONLINE_STATUS)} "
            "for selected characters from EVE server"
        )
    )
    def update_online_status(self, request, queryset):
        section = Character.UpdateSection.ONLINE_STATUS
        for obj in queryset:
            tasks.update_character_section.delay(character_pk=obj.pk, section=section)
            self.message_user(
                request,
                f"Started updating {Character.UpdateSection.display_name(section)} for character: {obj}. ",
            )

    inlines = (SyncStatusAdminInline,)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "_name", "_type", "_group", "_solar_system", "updated_at")
    list_filter = (
        ("eve_type__eve_group__eve_category", admin.RelatedOnlyFieldListFilter),
        ("eve_type__eve_group", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = [
        "id",
        "name",
        "eve_solar_system__eve_constellation__eve_region__name",
        "eve_type__name",
    ]
    list_select_related = (
        "eve_type__eve_group",
        "eve_type",
        "eve_solar_system__eve_constellation__eve_region",
        "eve_solar_system",
    )
    ordering = ["id"]

    @admin.display(ordering="name")
    def _name(self, obj):
        return obj.name_plus

    @admin.display(ordering="eve_solar_system__name")
    def _solar_system(self, obj):
        return obj.eve_solar_system.name if obj.eve_solar_system else None

    @admin.display(ordering="eve_type__name")
    def _type(self, obj):
        return obj.eve_type.name if obj.eve_type else None

    @admin.display(ordering="eve_type__eve_group__name")
    def _group(self, obj):
        return obj.eve_type.eve_group.name if obj.eve_type else None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SkillSetGroup)
class SkillSetGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "_skill_sets", "is_doctrine", "is_active")
    list_filter = (
        "is_doctrine",
        "is_active",
        ("skill_sets", admin.RelatedOnlyFieldListFilter),
    )
    ordering = ["name"]
    filter_horizontal = ("skill_sets",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related(
            Prefetch(
                "skill_sets",
                queryset=SkillSet.objects.order_by("name"),
                to_attr="skill_sets_ordered",
            )
        )

    def _skill_sets(self, obj):
        return format_html("<br>".join([x.name for x in obj.skill_sets_ordered]))


class MinValidatedInlineMixIn:
    validate_min = True

    def get_formset(self, *args, **kwargs):
        return super().get_formset(validate_min=self.validate_min, *args, **kwargs)


class SkillSetSkillAdminFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            try:
                data = self.cleaned_data
            except AttributeError:
                pass
            else:
                for row in data:
                    if (
                        row
                        and row.get("DELETE") is False
                        and not row.get("required_level")
                        and not row.get("recommended_level")
                    ):
                        eve_type = row.get("eve_type")
                        raise ValidationError(
                            f"Skill '{eve_type.name}' must have a level."
                        )


class SkillSetSkillAdminInline(MinValidatedInlineMixIn, admin.TabularInline):
    model = SkillSetSkill
    verbose_name = "skill"
    verbose_name_plural = "skills"
    min_num = 1
    formset = SkillSetSkillAdminFormSet
    autocomplete_fields = ("eve_type",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("eve_type", "skill_set__ship_type")

    # def get_formset(self, *args, **kwargs):
    #     formset = super().get_formset(*args, **kwargs)
    #     qs = formset.form.base_fields["skill_set"].queryset
    #     qs = qs.select_related("skill_set__ship_type__eve_group")
    #     formset.form.base_fields["skill_set"].queryset = qs
    #     return formset


# class SkillSetShipTypeFilter(admin.SimpleListFilter):
#     title = "is ship type"
#     parameter_name = "is_ship_type"

#     def lookups(self, request, model_admin):
#         return (
#             ("yes", "yes"),
#             ("no", "no"),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == "yes":
#             return SkillSet.objects.filter(ship_type__isnull=False)
#         if self.value() == "no":
#             return SkillSet.objects.filter(ship_type__isnull=True)
#         return SkillSet.objects.all()


@admin.register(SkillSet)
class SkillSetAdmin(admin.ModelAdmin):
    autocomplete_fields = ("ship_type",)
    list_display = (
        "name",
        "ship_type",
        "_skills",
        "_groups",
        "is_visible",
    )
    list_filter = (
        # SkillSetShipTypeFilter,  # this filter disables the prefetch in get_queryset
        ("groups", admin.RelatedOnlyFieldListFilter),
        "is_visible",
    )
    # list_select_related = ("ship_type",)
    ordering = ["name"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("ship_type").prefetch_related(
            Prefetch(
                "skills",
                queryset=SkillSetSkill.objects.select_related("eve_type").order_by(
                    "eve_type__name"
                ),
                to_attr="skills_ordered",
            ),
            Prefetch(
                "groups",
                queryset=SkillSetGroup.objects.order_by("name"),
                to_attr="groups_ordered",
            ),
        )

    def _skills(self, obj):
        return [
            "{} {} {}".format(
                skill.eve_type.name,
                skill.required_level if skill.required_level else "",
                f"[{skill.recommended_level}]" if skill.recommended_level else "",
            )
            for skill in obj.skills_ordered
        ]

    def _groups(self, obj) -> list:
        groups = [f"{group.name}" for group in obj.groups_ordered]
        return groups if groups else None

    inlines = (SkillSetSkillAdminInline,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ship_type":
            kwargs["queryset"] = (
                EveType.objects.select_related("eve_group__eve_category")
                .filter(eve_group__eve_category=EveCategoryId.SHIP)
                .order_by("name")
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
        tasks.update_characters_skill_checks.delay(force_update=True)

    def delete_model(self, request, obj):
        obj.user = request.user
        super().delete_model(request, obj)
        tasks.update_characters_skill_checks.delay(force_update=True)
