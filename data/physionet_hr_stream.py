# data/physionet_hr_stream.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator
import os

import numpy as np
import wfdb


@dataclass
class HRStream:
    """
    Produce a 1Hz (once-per-second) heart-rate stream (bpm) from a PhysioNet WFDB record.

    Uses MIT-BIH 'atr' annotations (beat locations) to compute RR intervals -> bpm,
    then interpolates bpm onto a 1-second timeline.

    record_name: "100", "101", ...
    base_dir: folder containing WFDB files (e.g., data/raw/mitdb)
    """
    record_name: str = "100"
    base_dir: str = "data/raw/mitdb"
    ann_ext: str = "atr"

    def iter_bpm_1hz(self, loop: bool = True) -> Iterator[int]:
        record_path = os.path.join(self.base_dir, self.record_name)

        #read header/dat for sampling rate, and atr for beat locations
        rec = wfdb.rdrecord(record_path)
        ann = wfdb.rdann(record_path, self.ann_ext)

        fs = float(rec.fs)
        rpeaks_sec = np.asarray(ann.sample, dtype=np.float64) / fs

        if rpeaks_sec.size < 2:
            raise ValueError(f"Record {self.record_name} has too few beats to compute HR.")

        #beat-to-beat HR at midpoints between beats
        rr = np.diff(rpeaks_sec)                 # seconds between beats
        bpm = 60.0 / rr
        t_mid = (rpeaks_sec[:-1] + rpeaks_sec[1:]) / 2.0

        # 1 Hz timeline
        t_end = float(rpeaks_sec[-1])
        t_grid = np.arange(0.0, t_end, 1.0)

        #interpolate HR onto the 1 Hz grid
        bpm_1hz = np.interp(t_grid, t_mid, bpm)

        #clamp to sane display range (prevents rare annotation artifacts from spiking UI)
        bpm_1hz = np.clip(bpm_1hz, 30, 220).astype(int)

        while True:
            for v in bpm_1hz:
                yield int(v)
            if not loop:
                break