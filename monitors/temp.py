import time
import random

def updateTemp(temp):
    change = random.uniform(-0.1, 0.1)
    temp = round(temp + change, 1)
    return max(96.0, min(temp, 103.0))

#while True:
    #current_temp = update_temp(current_temp)
   # print(f"Temp: {current_temp}°F")
 #   time.sleep(1)
