import random
import time

def respRate():
    resp = random.randint(12, 20)
    return resp

while True:
    resp = respRate()
    print("Respiratory Rate: ", resp, "Bpm")
    time.sleep(1)