import time

from pytube import YouTube
from moviepy.editor import *
from pytube import Playlist
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# Ref :https://stackoverflow.com/questions/68945080/pytube-exceptions-regexmatcherror-get-throttling-function-name-could-not-find


def convert_mp4_to_mp3(input_file_path: str, output_file_path: str = None, is_replace=True):
    if not output_file_path:
        output_file_path = input_file_path
    output_file_path.replace("mp4", "mp3")

    while not os.path.isfile(input_file_path):
        time.sleep(0.1)

    video_clip = VideoFileClip(input_file_path)
    video_clip.audio.write_audiofile(output_file_path)

    if is_replace and os.path.isfile(input_file_path):
        os.remove(input_file_path)


def video_download(video: YouTube, output_path: str):
    stream = video.streams.filter(progressive=True, file_extension="mp4").first()
    stream.download(output_path=output_path, filename=f"{video.title}.mp4")


if __name__ == "__main__":
    while True:
        download_source_type = input("input a download source type (video or playlist): ")

        url = input("input a video url: ")
        file_type = input("input a download extension (mp4 or mp3): ")
        output_path = input("input a download path ( ex: music/ ): ")

        if download_source_type == "video":
            video = YouTube(url)
            video_download(video, output_path)

            if file_type == "mp3":
                file_path = f"music/{video.title}.mp4"
                convert_mp4_to_mp3(file_path)


        elif download_source_type == "playlist":
            p = Playlist(url)

            for video in p.videos:
                video_download(video, output_path)

                if file_type == "mp3":
                    file_path = f"music/{video.title}.mp4"
                    convert_mp4_to_mp3(file_path)