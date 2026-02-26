import random
import time

currRespRate = random.randint(12, 20)

def updateRespRate(rr):
    change = random.randint(-1, 1)
    resp = rr + change
    return resp

#while True:
   # resp = updateRespRate(currRespRate)
   # print(f"Respiratory Rate: {resp} BPM")
   # time.sleep(1)