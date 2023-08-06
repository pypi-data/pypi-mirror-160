from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.utils.html import format_html

from allianceauth.services.hooks import get_extension_logger
from app_utils.logging import LoggerAddTag

from .. import __title__, tasks
from ..app_settings import MEMBERAUDIT_DATA_EXPORT_MIN_UPDATE_AGE
from ..core import data_exporters
from ..models import Character
from ._common import add_common_context

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required
@permission_required("memberaudit.exports_access")
def data_export(request):
    topics = data_exporters.topics_and_export_files()
    context = {
        "page_title": "Data Export",
        "topics": topics,
        "character_count": Character.objects.count(),
        "minutes_until_next_update": MEMBERAUDIT_DATA_EXPORT_MIN_UPDATE_AGE,
    }
    return render(
        request, "memberaudit/data_export.html", add_common_context(request, context)
    )


@login_required
@permission_required("memberaudit.exports_access")
def download_export_file(request, topic: str) -> FileResponse:
    exporter = data_exporters.DataExporter.create_exporter(topic)
    destination = data_exporters.default_destination()
    zip_file = destination / exporter.output_basename.with_suffix(".zip")
    if not zip_file.exists():
        raise Http404(f"Could not find export file for {topic}")
    logger.info("Returning file %s for download of topic %s", zip_file, topic)
    return FileResponse(zip_file.open("rb"))


@login_required
@permission_required("memberaudit.exports_access")
def data_export_run_update(request, topic: str):
    tasks.export_data_for_topic.delay(topic=topic, user_pk=request.user.pk)
    format_html
    messages.info(
        request,
        format_html(
            "Data export for topic <strong>{}</strong> has been started. "
            "This can take a couple of minutes. "
            "You will get a notification once it is completed.",
            topic,
        ),
    )
    return redirect("memberaudit:data_export")
