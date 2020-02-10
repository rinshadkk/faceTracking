import time
import RPi.GPIO as io
import tty, sys

tty.setraw(sys.stdin.fileno())

while True:
    ch = sys.stdin.read(1)
    print ch
    #if ch == 'a':
    #print "Wohoo"
    #if 
