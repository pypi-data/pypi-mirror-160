from pathlib import Path

from django.http import FileResponse
from rest_framework.views import APIView
from tailhead import tail

from log_api import settings


def tail_logs(log_file: Path, tail_lines):
    """

    @param log_file: the actual log file path
    @param tail_lines: tail lines of log file
    @return: stream content
    """
    yield b"\n".join(tail(log_file.open("rb"), tail_lines))


class DownloadView(APIView):
    permission_classes = settings.LOG_API_PERMISSION_CLASSES

    def get(self, request):
        log_name: str = self.request.query_params.get("name")
        if log_name and log_name.count(".") != 1:
            log_name += ".log"
        else:
            log_name = settings.LOG_API_DEFAULT_FILE

        file: Path = settings.LOG_API_DIR_PATH / log_name

        try:
            tail_lines: int = self.request.query_params.get("tail")
            if tail_lines is not None:
                tail_lines = int(tail_lines)
        except ValueError:
            tail_lines: int = settings.LOG_API_MAX_READ_LINES

        response = (
            FileResponse(file.open("rb"))
            if tail_lines is None
            else FileResponse(tail_logs(file, tail_lines))
        )

        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = f'attachment;filename="{log_name}"'
        return response
