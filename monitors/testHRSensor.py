from smbus2 import SMBus
import time
from collections import deque
import sys

ADDR = 0x57
bus = SMBus(1)

# ----------------------------
# MAX30102 SETUP
# ----------------------------
def setup_max30102():
    bus.write_byte_data(ADDR, 0x09, 0x40)  # reset
    time.sleep(0.1)
    bus.write_byte_data(ADDR, 0x09, 0x03)  # SpO2 mode
    bus.write_byte_data(ADDR, 0x0C, 0x2F)  # RED LED
    bus.write_byte_data(ADDR, 0x0D, 0x2F)  # IR LED
    bus.write_byte_data(ADDR, 0x0A, 0x4F)  # 100Hz internal
    bus.write_byte_data(ADDR, 0x04, 0)
    bus.write_byte_data(ADDR, 0x05, 0)
    bus.write_byte_data(ADDR, 0x06, 0)

def read_ir():
    d = bus.read_i2c_block_data(ADDR, 0x07, 6)
    return ((d[0] & 0x03) << 16) | (d[1] << 8) | d[2]

# ----------------------------
# MAIN
# ----------------------------
def main():
    setup_max30102()
    print("Place finger on sensor (Ctrl+C to quit)")
    time.sleep(1)

    fs = 20.0
    dt = 1.0 / fs

    window = deque(maxlen=int(fs * 1.0))  # 1 second window
    beat_times = deque(maxlen=5)

    MIN_AMP = 1000

    last_signal = 0
    last_bpm = None
    last_display = time.time()

    while True:
        t0 = time.time()

        signal = read_ir()
        window.append(signal)

        # ----------------------------
        # FINGER DETECTION
        # ----------------------------
        if len(window) >= 10:
            amp = max(window) - min(window)
            finger_present = amp >= MIN_AMP
        else:
            finger_present = False

        # ----------------------------
        # BEAT DETECTION (ZERO CROSS)
        # ----------------------------
        if finger_present:
            if last_signal > 0 and signal < last_signal:
                now = time.time()
                if not beat_times or now - beat_times[-1] > 0.4:
                    beat_times.append(now)
        else:
            beat_times.clear()
            last_bpm = None

        last_signal = signal

        # ----------------------------
        # BPM CALC (ONCE PER SECOND)
        # ----------------------------
        now = time.time()
        if now - last_display >= 1.0:
            last_display = now

            if not finger_present:
                msg = "NO FINGER"
            elif len(beat_times) >= 2:
                intervals = [
                    beat_times[i] - beat_times[i - 1]
                    for i in range(1, len(beat_times))
                ]
                avg_interval = sum(intervals) / len(intervals)
                bpm = round(60 / avg_interval)
                last_bpm = bpm
                msg = f"{bpm} BPM"
            else:
                msg = "MEASURING..."

            sys.stdout.write("\r" + msg + " " * 20)
            sys.stdout.flush()

        # ----------------------------
        # TIMING
        # ----------------------------
        sleep = dt - (time.time() - t0)
        if sleep > 0:
            time.sleep(sleep)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
