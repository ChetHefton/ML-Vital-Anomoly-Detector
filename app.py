import os
import time
import threading
import numpy as np
import wfdb
from wfdb import processing
from flask import Flask, jsonify, render_template

#importing classes and logic
from data.physionet_hr_stream import HRStream
from monitors import ox, respRate, temp

app = Flask(__name__)
lock = threading.Lock()

#setup the streamer for the calculated hr number
streamer = HRStream(record_name="100", base_dir="data/raw/mitdb")
hr_gen = streamer.iter_bpm_1hz()

#load the raw signal for the smooth wave graph
#mit-bih records have two channels
record_path = os.path.join("data/raw/mitdb", "100")
raw_rec = wfdb.rdrecord(record_path)

raw_fs = float(raw_rec.fs)
ecg = raw_rec.p_signal[:, 0].astype(float)

raw_signal_hr = ecg.tolist()

def bandpass_fft(x, fs, f_lo, f_hi):
    x = np.asarray(x, dtype=float)
    x = x - np.mean(x)
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(len(x), d=1.0 / fs)
    mask = (freqs >= f_lo) & (freqs <= f_hi)
    X *= mask
    y = np.fft.irfft(X, n=len(x))
    return y

def estimate_rr_bpm_from_edr(edr_window, fs, f_lo=0.1, f_hi=0.7):
    x = np.asarray(edr_window, dtype=float)
    if len(x) < int(fs * 10):
        return None
    
    x = x - np.mean(x)
    #apply Hanning window
    windowed_x = x * np.hanning(len(x))
    
    #zero padding: force the FFT to calculate 1024 points instead of 120
    #this changes the resolution from ~2 BPM to ~0.2 BPM
    n_fft = 1024 
    X = np.fft.rfft(windowed_x, n=n_fft)
    
    #calculate frequencies based on the new padded length
    freqs = np.fft.rfftfreq(n_fft, d=1.0 / fs)
    
    band = (freqs >= f_lo) & (freqs <= f_hi)
    if not np.any(band):
        return None
    
    mag = np.abs(X)
    peak_f = freqs[band][np.argmax(mag[band])]
    
    return float(peak_f * 60.0)

#detect peaks
rpeaks = wfdb.processing.gqrs_detect(sig=ecg, fs=raw_fs)

#correct peaks, gqrs sometimes marks the slope, this snaps them to the true max
rpeaks = wfdb.processing.correct_peaks(
    sig=ecg, 
    peak_inds=rpeaks, 
    search_radius=int(raw_fs * 0.05), 
    smooth_window_size=int(raw_fs * 0.05)
)

t_r = rpeaks / raw_fs

# baseline subtraction for amplitude look a few samples back to find the floor
a_r = []
for p in rpeaks:
    #look ~100ms before the peak to find the local baseline voltage
    baseline_idx = max(0, p - int(raw_fs * 0.1))
    local_baseline = ecg[baseline_idx]
    #amplitude is the height of the peak minus the local baseline
    a_r.append(ecg[p] - local_baseline)

a_r = np.array(a_r)

edr_fs = 4.0
t_edr = np.arange(0, len(ecg) / raw_fs, 1.0 / edr_fs)
edr = np.interp(t_edr, t_r, a_r)

edr_filt = bandpass_fft(edr, edr_fs, f_lo=0.1, f_hi=0.7)
edr_filt = (edr_filt - np.mean(edr_filt)) / (np.std(edr_filt) + 1e-9)

display_fs = 20.0
t_disp = np.arange(0, t_edr[-1], 1.0 / display_fs)
edr_disp = np.interp(t_disp, t_edr, edr_filt)
raw_signal_rr = edr_disp.tolist()

#global state for tracking where we are in the signal
signal_index = 0
rr_index = 0

#shared vitals state
vitals = {
    "hr": 0,
    "hr_wave": [],
    "spo2": 98.0,
    "rr": 16,
    "temp_f": 98.6,
    "ts": "",
    "rr_wave": []
}

#global counter to sync the 1hz data with the 20hz loop
frame_counter = 0

def updater_loop():
    global signal_index, rr_index, frame_counter
    while True:
        with lock:
            chunk_size = int(raw_fs * 0.05)
            rr_chunk_size = int(display_fs * 0.05)

            chunk_hr = raw_signal_hr[signal_index : signal_index + chunk_size]
            if len(chunk_hr) < chunk_size:
                chunk_hr += raw_signal_hr[0 : (chunk_size - len(chunk_hr))]
            vitals["hr_wave"] = chunk_hr

            chunk_rr = raw_signal_rr[rr_index : rr_index + rr_chunk_size]
            if len(chunk_rr) < rr_chunk_size:
                chunk_rr += raw_signal_rr[0 : (rr_chunk_size - len(chunk_rr))]
            vitals["rr_wave"] = chunk_rr

            signal_index = (signal_index + chunk_size) % len(raw_signal_hr)
            rr_index = (rr_index + rr_chunk_size) % len(raw_signal_rr)

            if frame_counter % int(display_fs) == 0:
                vitals["hr"] = next(hr_gen)

                rr_est_window_sec = 30
                rr_est_n = int(edr_fs * rr_est_window_sec)

                t_now = signal_index / raw_fs
                edr_now_idx = int(t_now * edr_fs) % len(edr_filt)

                if edr_now_idx >= rr_est_n:
                    window = edr_filt[edr_now_idx - rr_est_n : edr_now_idx]
                else:
                    tail = edr_filt[len(edr_filt) - (rr_est_n - edr_now_idx) :]
                    head = edr_filt[:edr_now_idx]
                    window = np.concatenate([tail, head])

                rr_bpm = estimate_rr_bpm_from_edr(window, edr_fs, f_lo=0.1, f_hi=0.7)
                if rr_bpm is not None:
                    vitals["rr"] = int(np.clip(rr_bpm, 8, 35))
                else:
                    vitals["rr"] = 16

                vitals["spo2"] = ox.updateOx(vitals.get("spo2", 98.0))
                vitals["temp_f"] = temp.updateTemp(vitals.get("temp_f", 98.6))
                vitals["ts"] = time.strftime("%H:%M:%S")
                frame_counter = 0

            frame_counter += 1
        time.sleep(0.05)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/vitals")
def api_vitals():
    with lock:
        return jsonify(vitals)

if __name__ == "__main__":
    t = threading.Thread(target=updater_loop, daemon=True)
    t.start()
    app.run(host="127.0.0.1", port=5000, debug=True)