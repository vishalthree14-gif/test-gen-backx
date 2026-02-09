import imageio_ffmpeg
import subprocess

def generate_thumbnail(video_path, thumbnail_path):
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg_path,
        "-i", video_path,
        "-ss", "00:00:03",
        "-vframes", "1",
        thumbnail_path
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
