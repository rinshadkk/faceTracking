import time
import RPi.GPIO as io

io.cleanup()

io.setmode(io.BCM)

power_pin = 22

io.setup(power_pin,io.OUT)
io.output(power_pin,False)

while True:
	io.output(power_pin, True)
	time.sleep(0.050)
	io.output(power_pin, False)
	time.sleep(0.050)
