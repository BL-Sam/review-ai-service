from faster_whisper import WhisperModel


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(audio_path: str) -> str:
    segments, _ = model.transcribe(audio_path)

    transcript_parts = []

    for segment in segments:
        transcript_parts.append(segment.text)

    return " ".join(transcript_parts)