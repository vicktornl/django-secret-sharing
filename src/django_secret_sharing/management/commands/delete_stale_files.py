import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from django_secret_sharing.models import File
from django_secret_sharing.utils import get_backend

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete stale (expired and unfinished) files."

    def handle(self, *args, **options):
        now = timezone.now()
        expired_files = File.objects.filter(secret__expires_at__lte=now)
        existing_file_refs = list(File.objects.values_list("ref", flat=True))
        backend = get_backend()
        deleted_files_refs = backend.delete_stale_files(
            expired_files, existing_file_refs
        )

        if len(deleted_files_refs):
            for file_ref in deleted_files_refs:
                logger.info("Deleted file %s" % file_ref)
        else:
            logger.info("No stale files to delete")
