import random
import time

def heart_rate():
	return random.randint(50,150)

while True:
	bpm = heart_rate()
	print(bpm)
	time.sleep(1)

