from django.conf import settings
from rest_framework.settings import api_settings

LOG_READER_DIR_PATH = getattr(
    settings, "LOG_READER_DIR_PATH", getattr(settings, "BASE_DIR") / "logs"
)
LOG_READER_DEFAULT_FILE = getattr(settings, "LOG_READER_DEFAULT_FILE", "django.log")
LOG_READER_MAX_READ_LINES = getattr(settings, "LOG_READER_MAX_READ_LINES", 1000)
LOG_PERMISSION_CLASSES = getattr(
    settings, "LOG_PERMISSION_CLASSES", api_settings.DEFAULT_PERMISSION_CLASSES
)
