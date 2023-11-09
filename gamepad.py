# from https://github.com/adafruit/Adafruit_CircuitPython_seesaw/blob/main/examples/seesaw_gamepad_qt.py

from machine import Pin, I2C
import struct, time
import time

GamePad = 0x50
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
print([hex(i) for i in i2c.scan()])

ADC_BASE = 0x09
ADC_OFFSET = 0x07
GPIO_BASE = 0x01
GPIO_BULK = 0x04
GPIO_DIRCLR_BULK = 0x03
GPIO_PULLENSET = 0x0B
GPIO_BULK_SET = 0x05

#X button corresponds to bit 6
BTN_CONST = [1 << 6, 1 << 2, 1 << 5, 1 << 1, 1 << 0, 1 << 16]
BTN_Value = ['x','y','A','B','select','start']
BTN_Mask = 0
for btn in BTN_CONST:
    BTN_Mask |=  btn
    
def digital_setup():
    cmd = bytearray(4)
    cmd[0:] = struct.pack(">I", BTN_Mask)
    buffer = bytearray([GPIO_BASE, GPIO_DIRCLR_BULK]) + cmd
    reply = i2c.writeto(GamePad,buffer)
    buffer = bytearray([GPIO_BASE, GPIO_PULLENSET]) + cmd
    reply = i2c.writeto(GamePad,buffer)
    buffer = bytearray([GPIO_BASE, GPIO_BULK_SET]) + cmd
    reply = i2c.writeto(GamePad,buffer)
    
def digital_read(delay=0.008):
    '''Get the values of all the pins on the "B" port as a bitmask'''
    buffer = bytearray([GPIO_BASE, GPIO_BULK])
    buf = i2c.writeto(GamePad,buffer)
    time.sleep(delay)
    buf = i2c.readfrom(GamePad,4)
    try:
        ret = struct.unpack(">I", buf)[0]
    except OverflowError:
        buf[0] = buf[0] & 0x3F
        ret = struct.unpack(">I", buf)[0]
    return ret & BTN_Mask

def read_joystick(pin, delay = 0.008):
    '''Read an analog signal from the game pad - define both the pin and a delay between write and read'''
    reply = i2c.writeto(GamePad,bytearray([ADC_BASE, ADC_OFFSET + pin]))
    time.sleep(delay)
    reply = i2c.readfrom(GamePad,2)
    return struct.unpack('>H',reply)[0]
