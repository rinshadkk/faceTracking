import time
import RPi.GPIO as io
import tty, sys

tty.setraw(sys.stdin.fileno())

io.setmode(io.BCM)

power_pin = 23
power_pin2 = 24

motor2_pin1 = 27
motor2_pin2 = 17

io.setup(power_pin,io.OUT)
io.setup(power_pin2,io.OUT)
io.setup(motor2_pin1,io.OUT)
io.setup(motor2_pin2,io.OUT)

io.output(power_pin,False)
io.output(power_pin2,False)
while True:
    ch = sys.stdin.read(1)
    if ch == 'a':
        print "Wohoo"
        io.output(power_pin,False)
        io.output(power_pin2,False)
        #time.sleep(0.50)
        io.output(power_pin, True)
        io.output(power_pin2,False)

    if ch == 's':
        print(ch)
        io.output(power_pin,False)
        io.output(power_pin2,False)
        #time.sleep(0.050)
        io.output(power_pin, False)
        io.output(power_pin2,True)
        
    if ch == 'z':
        print(ch)
        io.output(motor2_pin1,False)
        io.output(motor2_pin2,False)
        #time.sleep(0.050)
        io.output(motor2_pin1, False)
        io.output(motor2_pin2,True)

    if ch == 'x':
        print(ch)
        io.output(motor2_pin1,False)
        io.output(motor2_pin2,False)
        #time.sleep(0.050)
        io.output(motor2_pin1, True)
        io.output(motor2_pin2,False)
    
    if ch == 'q':
        break
