import os

from storages.backends.s3boto3 import S3Boto3Storage


class SupabaseMediaStorage(S3Boto3Storage):
    """Media storage on Supabase Storage.

    Uploads via Supabase S3-compatible endpoint, serves via public object URL.
    Requires the bucket to be public for unauthenticated reads.
    """

    bucket_name = os.environ.get("SUPABASE_STORAGE_BUCKET", "")

    # Use public URL for serving (works for public buckets)
    _project_ref = os.environ.get("SUPABASE_PROJECT_REF", "")
    if _project_ref and bucket_name:
        custom_domain = f"{_project_ref}.supabase.co/storage/v1/object/public/{bucket_name}"

    querystring_auth = False
    file_overwrite = True
