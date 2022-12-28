"""Main module for the streamlit template app"""
import streamlit as st
import subprocess

import pandas as pd
import os
from io import *
from analysis import *
import tempfile


def main():
    input_video = st.file_uploader("Upload Video")
    if input_video is not None:
        os.makedirs("temp_data", exist_ok=True)
        video_fn = os.path.join("temp_data", input_video.name)
        with open(video_fn, "wb") as f:
            f.write(input_video.getbuffer())
        video_basename, video_ext = os.path.splitext(input_video.name)
        print(video_basename, video_ext)
        audio_fn = os.path.join("temp_data", f"{video_basename}.wav")
        print(os.getcwd())
        cmd = f"ffmpeg -i {video_fn} -map 0:a {audio_fn}"
        print(cmd)
        subprocess.run(cmd, shell=True)
        denoised_video_fn = os.path.join(
            "temp_data", f"{video_basename}.denoised{video_ext}"
        )
        denoised_audio_fn = denoise(audio_fn)
        print("=" * 300)
        print(f"Combining video and audio at {denoised_video_fn}")
        cmd = f"ffmpeg -i {video_fn} -i {denoised_audio_fn} -c:v copy -map 0:v:0 -map 1:a:0 {denoised_video_fn}"

        subprocess.run(cmd, shell=True)
        print("Video and audio combined!.")
        st.header("New Video")
        st.video(os.path.join(os.getcwd(), denoised_video_fn), format="video/mp4")

        st.header("Old Video")
        st.video(input_video, format="video/mp4")


if __name__ == "__main__":
    main()
