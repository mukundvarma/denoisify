"""Main module for the streamlit template app"""
import streamlit as st
import subprocess

import pandas as pd
import os
from io import *
from analysis import *
import tempfile
import logging


def main():
    st.header("Denoisiy 🔇")
    st.subheader("Remove background noise from videos.")
    input_video = st.file_uploader("Upload Video", type=["mp4"])
    if input_video is not None:
        os.makedirs("temp_data", exist_ok=True)
        orig_fn = input_video.name
        video_basename, video_ext = os.path.splitext(orig_fn)
        video_name = "".join(x for x in video_basename if x.isalnum())
        video_fn = os.path.join("temp_data", f"{video_name}{video_ext}")

        with st.spinner("Reading input file."):
            with open(video_fn, "wb") as f:
                f.write(input_video.getbuffer())
        audio_fn = os.path.join("temp_data", f"{video_name}.wav")
        cmd = f"ffmpeg -i {video_fn} -map 0:a {audio_fn}"
        logging.debug(cmd)
        with st.spinner("Extracting audio."):
            subprocess.run(cmd, shell=True)
            denoised_video_fn = os.path.join(
                "temp_data", f"{video_name}.denoised{video_ext}"
            )
        st.info("Audio extraction complete.")
        with st.spinner("Denoising audio."):
            denoised_audio_fn = denoise(audio_fn)
        st.info("Video denoising complete.")
        with st.spinner(f"Combining video and audio at {denoised_video_fn}"):
            cmd = f"ffmpeg -i {video_fn} -i {denoised_audio_fn} -c:v copy -map 0:v:0 -map 1:a:0 {denoised_video_fn}"
            subprocess.run(cmd, shell=True)
        st.info("Denoisification complete!")
        st.balloons()
        st.subheader("Original Video")
        st.video(input_video, format="video/mp4")
        st.subheader("New Video")
        st.video(os.path.join(os.getcwd(), denoised_video_fn), format="video/mp4")


if __name__ == "__main__":
    main()
