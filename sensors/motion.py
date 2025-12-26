import random
import time

def isMotion():
    isMotion = random.randint(1,10)
    if isMotion > 1:
        return False
    else:
        return True

while True:
    motion = isMotion()
    print("Motion Detected: ", motion)
    time.sleep(1)  