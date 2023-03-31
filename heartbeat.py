import RPi.GPIO as GPIO
import time
import atexit
GPIO.setmode(GPIO.BOARD)
heartbeat = 16 #GPIO 23

GPIO.setup(heartbeat, GPIO.OUT)
#GPIO.output(heartbeat, GPIO.HIGH)

def exit_handler():
    GPIO.output(heartbeat, GPIO.LOW)
atexit.register(exit_handler)
while(True):
    GPIO.output(heartbeat, GPIO.HIGH)
    time.sleep(5.2)
    GPIO.output(heartbeat, GPIO.LOW)
    time.sleep(0.2)
    print('Heart Beat trigger sent')
    time.sleep(2)

