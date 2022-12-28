from sklearn.model_selection import GridSearchCV
import os
import subprocess
import tempfile
import noisereduce as nr
from maad.sound import (
    spectrogram,
    sharpness,
    temporal_snr,
    spectral_snr,
    avg_power_spectro,
)
import numpy as np
from scipy.io import wavfile

from sklearn.base import BaseEstimator, TransformerMixin

SPEECH_FREQUENCY_RANGE = [100, 350]
PARAM_GRID_NS = {
    "stationary": [False],
    "sigmoid_slope_nonstationary": [5, 10],
    "time_constant_s": [1, 2],
    "n_fft": [512],
    "freq_mask_smooth_hz": [200, 1000],
}
PARAM_GRID_S = {
    "stationary": [True],
    "n_std_thresh_stationary": [1, 3],
    "n_fft": [512],
    "freq_mask_smooth_hz": [200, 1000],
}


class Denoiser(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        sr,
        stationary=False,
        prop_decrease=0.9,
        time_constant_s=1.0,
        freq_mask_smooth_hz=500,
        time_mask_smooth_ms=50,
        thresh_n_mult_nonstationary=1,
        sigmoid_slope_nonstationary=10,
        n_std_thresh_stationary=1.5,
        n_fft=512,
    ):
        """
        rate : int
            sample rate of input signal / noise signal
        y_noise : np.ndarray [shape=(# frames,) or (# channels, # frames)], real-valued
            noise signal to compute statistics over (only for non-stationary noise reduction).
        stationary : bool, optional
            Whether to perform stationary, or non-stationary noise reduction, by default False
        prop_decrease : float, optional
            The proportion to reduce the noise by (1.0 = 100%), by default 1.0
        time_constant_s : float, optional
            The time constant, in seconds, to compute the noise floor in the non-stationary
            algorithm, by default 2.0
        freq_mask_smooth_hz : int, optional
            The frequency range to smooth the mask over in Hz, by default 500
        time_mask_smooth_ms : int, optional
            The time range to smooth the mask over in milliseconds, by default 50
        thresh_n_mult_nonstationary : int, optional
            Only used in nonstationary noise reduction., by default 1
        sigmoid_slope_nonstationary : int, optional
            Only used in nonstationary noise reduction., by default 10
        n_std_thresh_stationary : int, optional
            Number of standard deviations above mean to place the threshold between
            signal and noise., by default 1.5
          n_fft : int, optional
                length of the windowed signal after padding with zeros.
                The number of rows in the STFT matrix ``D`` is ``(1 + n_fft/2)``.
                The default value, ``n_fft=2048`` samples, corresponds to a physical
                duration of 93 milliseconds at a sample rate of 22050 Hz, i.e. the
                default sample rate in librosa. This value is well adapted for music
                signals. However, in speech processing, the recommended value is 512,
                corresponding to 23 milliseconds at a sample rate of 22050 Hz.
                In any case, we recommend setting ``n_fft`` to a power of two for
                optimizing the speed of the fast Fourier transform (FFT) algorithm., by default 1024
        """
        self.sr = sr
        self.stationary = stationary
        self.prop_decrease = prop_decrease
        self.time_constant_s = time_constant_s
        self.freq_mask_smooth_hz = freq_mask_smooth_hz
        self.time_mask_smooth_ms = time_mask_smooth_ms
        self.thresh_n_mult_nonstationary = thresh_n_mult_nonstationary
        self.sigmoid_slope_nonstationary = sigmoid_slope_nonstationary
        self.n_std_thresh_stationary = n_std_thresh_stationary
        self.n_fft = n_fft
        print("Init complete")

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        print("starting transform")
        nframes, nchannels = X.shape
        # todo: figure out how to deal with multiple channels
        denoised = nr.reduce_noise(
            y=X[:, 0],
            **self.get_params(),
            use_tqdm=True,
            chunk_size=3000,
        )
        print(len(denoised))
        return denoised

    def score(self, X, y=None):
        X_denoised = self.transform(X)
        metrics = calculate_metrics(X_denoised, self.sr)
        fn = metrics["spectrogram"][2]
        S = metrics["spectrogram"][0]
        power = np.median(
            avg_power_spectro(
                S[
                    :,
                    np.where(fn > SPEECH_FREQUENCY_RANGE[0])[0][0] : np.where(
                        fn < SPEECH_FREQUENCY_RANGE[1]
                    )[0][-1],
                ]
            )
        )
        print("finished score.")
        return metrics["temporal"][2] * metrics["spectral"][2] * np.sqrt(power)


def calculate_metrics(data, sr):
    t_snr = temporal_snr(data)
    spec = spectrogram(data, sr)
    s_snr = spectral_snr(spec[0])
    return {"temporal": t_snr, "spectral": s_snr, "spectrogram": spec}


def choose_best_denoiser(data, rate, param_grid):
    dn = Denoiser(rate)
    gcv = GridSearchCV(dn, param_grid, verbose=1)
    gcv.fit(data)
    denoised = gcv.best_estimator_.transform(data)
    score = gcv.best_estimator_.score(data)
    return denoised, score


def denoise(audio_file, grid_search=False):
    rate, data = wavfile.read(audio_file)
    basename, ext = os.path.splitext(audio_file)

    print("Starting to denoise.")
    if grid_search:
        print("Entering grid search.")
        best_stationary, s_score = choose_best_denoiser(data, rate, PARAM_GRID_S)
        best_nonstationary, ns_score = choose_best_denoiser(data, rate, PARAM_GRID_NS)
        best = best_nonstationary
        if ns_score < s_score:
            best = best_stationary
    else:
        print("Single denoiser.")
        dn = Denoiser(rate)
        best = dn.fit_transform(data)

    wavfile.write(f"{basename}.denoised.wav", rate, best)
    print("Denoised audio written.")

    return f"{basename}.denoised.wav"


def split_audio_and_video(video_fn):
    basen, ext = os.path.splitext(video_fn)
    audio_fn = f"{basen}.wav"
    cmd = f"ffmpeg -i {video_fn} -map 0:a -c:a aac {audio_fn}"
    subprocess.run(cmd)
    return audio_fn
