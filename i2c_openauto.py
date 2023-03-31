#!/usr/bin/env python3
import time
import colorsys
import ioexpander as io
import uinput
import atexit

#Change the I2C_ADDR to:
# - 0x0F to use with the Rotary Encoder breakout.
# - 0x18 to use with IO Expander.

I2C_ADDR = 0x0F  # 0x18 for IO Expander, 0x0F for the encoder breakout
#Pins for the rotary encoder breakout
PIN_RED = 1
PIN_GREEN = 7
PIN_BLUE = 2

POT_ENC_A = 12
POT_ENC_B = 3
POT_ENC_C = 11

BRIGHTNESS = 0.5                # Effectively the maximum fraction of the period that the LED will be on
PERIOD = int(255 / BRIGHTNESS)  # Add a period large enough to get 0-255 steps at the desired brightness
RGB_RATE= 0.005 #arbitrary value for how quickly colors change
ioe = io.IOE(i2c_addr=I2C_ADDR, interrupt_pin=4)

# Swap the interrupt pin for the Rotary Encoder breakout
if I2C_ADDR == 0x0F:
    ioe.enable_interrupt_out(pin_swap=True)

ioe.setup_rotary_encoder(1, POT_ENC_A, POT_ENC_B, pin_c=POT_ENC_C)

ioe.set_pwm_period(PERIOD)
ioe.set_pwm_control(divider=2)  # PWM as fast as we can to avoid LED flicker

ioe.set_mode(PIN_RED, io.PWM, invert=True)
ioe.set_mode(PIN_GREEN, io.PWM, invert=True)
ioe.set_mode(PIN_BLUE, io.PWM, invert=True)
# creating device for uinput with the keyboard inputs we're interested in
device = uinput.Device([
        uinput.KEY_F7, # Volume Down
        uinput.KEY_F8, # Volume up
        uinput.KEY_F9, # Brightness down
        uinput.KEY_F10, # Brightness up
        ])
print("Running LED with {} brightness steps.".format(int(PERIOD * BRIGHTNESS)))

count = 0
r, g, b, = 0, 0, 0
h=0
### initialise scripts
#flash led on startup
def enc_led_change(r,g,b):
    ioe.output(PIN_RED, r)
    ioe.output(PIN_GREEN, g)
    ioe.output(PIN_BLUE, b)
def exit_handler():
    enc_led_change(0,0,0)
atexit.register(exit_handler)
enc_led_change(0,0,0)
#run once to get initial value of encoder
if ioe.get_interrupt():
    current = ioe.read_rotary_encoder(1)
    ioe.clear_interrupt
    time.sleep(1/30)
    
while True:
    if ioe.get_interrupt():
        count = ioe.read_rotary_encoder(1)
        ioe.clear_interrupt()
    if count !=current:
        if count>current:
            #print("Volume Up")
            device.emit_click(uinput.KEY_F8)
        elif count < current:
            #print("Volume Down")
            device.emit_click(uinput.KEY_F7)
    #h = (count % 359) / 360.0  ##changes color based on rotation
    if h>=1: # loops colors
        h=0
    h+=RGB_RATE
    r, g, b = [int(c * PERIOD * BRIGHTNESS) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
    enc_led_change(r,g,b)

    print(count, r, g, b)
    current = count
    time.sleep(1.0 / 20)
