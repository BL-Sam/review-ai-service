# import tempfile
# from pathlib import Path
# from pydub import AudioSegment


# def convert_audio_to_wav(audio_bytes: bytes) -> str:
#     with tempfile.NamedTemporaryFile(
#         delete=False,
#         suffix=".mp3"
#     ) as temp_input:

#         temp_input.write(audio_bytes)
#         input_path = temp_input.name

#     output_path = Path(input_path).with_suffix(".wav")

#     audio = AudioSegment.from_file(input_path)

#     audio = audio.set_channels(1)
#     audio = audio.set_frame_rate(16000)

#     audio.export(
#         output_path,
#         format="wav"
#     )

#     return str(output_path)


import subprocess
import tempfile
from pathlib import Path


def convert_audio_to_wav(audio_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    ) as input_file:

        input_file.write(audio_bytes)
        input_path = input_file.name

    output_path = str(
        Path(input_path).with_suffix(".wav")
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path,
    ]

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return output_path