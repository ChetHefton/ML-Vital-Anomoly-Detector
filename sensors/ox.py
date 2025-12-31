import random
import time

currOx = round(random.uniform(95.0, 100.0), 1)

def updateOx(ox):
    change = random.uniform(-0.1, 0.1)
    ox += change
    ox = round(ox, 1)
    return max(90.0, min(ox, 100.0))

#while True:
  #  currOx = updateOx(currOx)
   # print(f"SpO₂: {currOx:.1f}%")
    #time.sleep(1)
