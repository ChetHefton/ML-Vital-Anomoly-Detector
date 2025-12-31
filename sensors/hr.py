import random
import time

currHR = random.randint(60, 100)

def updateHR(hr):
    change = random.choice([0, 0, -1, 1, -2, 2])
    hr += change
    return max(40, min(hr, 180))

#while True:
 #   currHR = updateHR(currHR)
  #  print(f"HR: {currHR} bpm")
   # time.sleep(1)
