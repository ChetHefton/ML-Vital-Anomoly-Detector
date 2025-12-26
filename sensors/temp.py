import time
import random

def temp():
    temp = round(random.uniform(96.6, 103.0), 1)
    return temp

while True:
    templvl = temp()
    print("Temperature: ", templvl)
    time.sleep(1)