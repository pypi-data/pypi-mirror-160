from pathlib import Path

from django.conf import settings
from rest_framework.settings import api_settings, perform_import

LOG_API_DIR_PATH = getattr(
    settings, "LOG_API_DIR_PATH", Path(getattr(settings, "BASE_DIR")) / "logs"
)
LOG_API_DEFAULT_FILE = getattr(settings, "LOG_API_DEFAULT_FILE", "django.log")
LOG_API_MAX_READ_LINES = getattr(settings, "LOG_API_MAX_READ_LINES", 1000)

LOG_API_PERMISSION_CLASSES = (
    perform_import(
        getattr(settings, "LOG_API_PERMISSION_CLASSES", None),
        "LOG_API_PERMISSION_CLASSES",
    )
    or api_settings.DEFAULT_PERMISSION_CLASSES
)
