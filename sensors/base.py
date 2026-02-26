import hr
import motion
import ox
import respRate
import temp
import time
import random
from collections import deque
import sys

WINDOW_SIZE = 10

#ANSI helpers
def clear_screen():
    sys.stdout.write("\033[2J\033[H")   #clear + cursor home
    sys.stdout.flush()

class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    RESET  = "\033[0m"

#rolling queues/columns
hr_q   = deque(maxlen=WINDOW_SIZE)
ox_q   = deque(maxlen=WINDOW_SIZE)
rr_q   = deque(maxlen=WINDOW_SIZE)
temp_q = deque(maxlen=WINDOW_SIZE)

#initial values
currHR   = random.randint(60, 100)
currOx   = round(random.uniform(95.0, 100.0), 1)
currRR   = random.randint(12, 20)
currTemp = round(random.uniform(97.0, 99.0), 1)

def color_hr(hr):
    if hr < 55 or hr > 110:
        return C.RED
    elif hr < 65 or hr > 95:
        return C.YELLOW
    return C.GREEN

def color_ox(ox):
    if ox < 90:
        return C.RED
    elif ox < 95:
        return C.YELLOW
    return C.GREEN

def color_rr(rr):
    if rr < 10 or rr > 24:
        return C.RED
    elif rr < 12 or rr > 20:
        return C.YELLOW
    return C.GREEN

def color_temp(t):
    if t < 96 or t > 100.4:
        return C.RED
    elif t < 97 or t > 99.5:
        return C.YELLOW
    return C.GREEN

def render():
    clear_screen()

    current_time = time.strftime("%a %b %d, %Y  %I:%M:%S %p")

    print("=== LIVE PATIENT MONITOR ===\n")
    print(f"Time: {current_time}\n")

    print(f"{color_hr(currHR)}HR   : {currHR:3} bpm{C.RESET}")
    print(f"{color_ox(currOx)}SpO2 : {currOx:4}%{C.RESET}")
    print(f"{color_rr(currRR)}RR   : {currRR:3} bpm{C.RESET}")
    print(f"{color_temp(currTemp)}Temp : {currTemp:4} F{C.RESET}")

    print("\n--- Rolling Data (last 10) ---")
    print(f"HR   : {list(hr_q)}")
    print(f"SpO2 : {list(ox_q)}")
    print(f"RR   : {list(rr_q)}")
    print(f"Temp : {list(temp_q)}")


while True:
    #update vitals
    currHR   = hr.updateHR(currHR)
    currOx   = ox.updateOx(currOx)
    currRR   = respRate.updateRespRate(currRR)
    currTemp = temp.updateTemp(currTemp)

    #push into queues
    hr_q.append(currHR)
    ox_q.append(currOx)
    rr_q.append(currRR)
    temp_q.append(currTemp)

    render()

    time.sleep(1)