import random
import time

def ox():
    oxlvl = random.randint(95,100)
    return oxlvl

while True:
    oxlvl = ox()
    print("SpO2: ", oxlvl, "%")
    time.sleep(1)