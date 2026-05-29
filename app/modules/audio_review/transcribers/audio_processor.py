from .audio_converter import convert_audio_to_wav
from .transcriber import transcribe_audio


def process_audio(audio_bytes: bytes) -> str:
    wav_path = convert_audio_to_wav(audio_bytes)

    transcript = transcribe_audio(wav_path)

    return transcript