from pathlib import Path
import requests

from app.core.config import settings
from app.core.exceptions.custom_exceptions import AudioDownloadException





def get_audio_bytes(audio_file_url: str) -> bytes:
    """
    DEV:
        Read audio from local path

    QA / PROD:
        Download audio from object storage URL
    """

    if settings.ENV.upper() == "DEV":
        return _load_from_local(audio_file_url)

    return _download_from_url(audio_file_url)


def _load_from_local(audio_file_url: str) -> bytes:
    """
    Example input:
        q1.mp3

    Resolves:
        LOCAL_AUDIO_BASE_PATH/q1.mp3
    """

    file_path = Path(
        settings.LOCAL_AUDIO_BASE_PATH
    ) / audio_file_url

    if not file_path.exists():
        raise AudioDownloadException(
            f"Local audio file not found: {file_path}"
        )

    with open(file_path, "rb") as file:
        return file.read()


def _download_from_url(audio_url: str) -> bytes:
    try:
        response = requests.get(
            audio_url,
            timeout=20
        )

        response.raise_for_status()

        return response.content

    except Exception as exc:
        raise AudioDownloadException(
            f"Unable to download audio file: {str(exc)}"
        )