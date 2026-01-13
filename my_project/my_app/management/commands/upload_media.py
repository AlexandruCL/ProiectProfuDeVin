from pathlib import Path

from django.core.files.base import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
	help = "Upload local MEDIA_ROOT files to configured default storage (e.g., Supabase)."

	def add_arguments(self, parser):
		parser.add_argument(
			"--source",
			default=None,
			help="Local source directory to upload (defaults to settings.MEDIA_ROOT).",
		)
		parser.add_argument(
			"--prefix",
			default="",
			help="Optional prefix to prepend to all uploaded keys.",
		)
		parser.add_argument(
			"--skip-existing",
			action="store_true",
			help="Skip files that already exist in storage.",
		)

	def handle(self, *args, **options):
		from django.conf import settings

		source = options["source"] or settings.MEDIA_ROOT
		prefix = options["prefix"].strip("/")
		skip_existing = options["skip_existing"]

		source_path = Path(source)
		if not source_path.exists():
			raise FileNotFoundError(f"Source folder not found: {source_path}")

		uploaded = 0
		skipped = 0

		for file_path in source_path.rglob("*"):
			if file_path.is_dir():
				continue

			rel = file_path.relative_to(source_path).as_posix()
			key = f"{prefix}/{rel}" if prefix else rel

			if skip_existing and default_storage.exists(key):
				skipped += 1
				continue

			with open(file_path, "rb") as fh:
				default_storage.save(key, File(fh))
			uploaded += 1

		self.stdout.write(
			self.style.SUCCESS(
				f"Uploaded {uploaded} files (skipped {skipped}) from {source_path}"
			)
		)
