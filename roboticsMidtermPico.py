from machine import ADC, Pin
import uasyncio as asyncio
import math
import time
import gamepad
import requests
import mqtt

#initalize gamepad
gamepad.digital_setup()

#move all of this to a secrets file or just comment out
adafruit_USER = "kkowalick25"
adafruit_KEY = "aio_radk08BuCxIyfdlih7ndr6zvRzh2"
Token_ID = "patqZmgFyuaf4TXNe"
Token_SECRET = "patqZmgFyuaf4TXNe.426312d34bf83c18ea9d85a4f0819cb9d4ed3bad5b63f82f4a1278fd3762aab9"

#initalize Adafruit Dashboard
url = 'https://io.adafruit.com/api/v2/%s/feeds' % adafruit_USER
headers = {'X-AIO-Key':adafruit_KEY,'Content-Type':'application/json'}
reply = requests.get(url,headers=headers)
print(reply)
if reply.status_code == 200:
    reply = reply.json() #a JSON array of info
    keys = [x['key'] for x in reply]
    groups = [x['group']['name'] for x in reply]
    names = [x['name'] for x in reply]
    values = [x['last_value'] for x in reply]
    ids = [x['id'] for x in reply]
else:
    print(f"Request failed with status code: {reply.status_code}")

#connect client to adafruit dashboard
client = mqtt.MQTTClient("KellisPico", "io.adafruit.com", 1883, user=adafruit_USER, password=adafruit_KEY, keepalive=60)
client.connect()

#initialize pins
thermistor = ADC(28)
tenLED = Pin(12, mode=Pin.OUT)
twentyLED = Pin(13, mode=Pin.OUT)
thirtyLED = Pin(4, mode=Pin.OUT)
fourtyLED = Pin(5, mode=Pin.OUT)
fiftyLED = Pin(6, mode=Pin.OUT)
sixtyLED = Pin(7, mode=Pin.OUT)
seventyLED = Pin(8, mode=Pin.OUT)
eightyLED = Pin(9, mode=Pin.OUT)
ninetyLED = Pin(10, mode=Pin.OUT)
hundredLED = Pin(11, mode=Pin.OUT)

def temperature_reading():
    temperature_value = thermistor.read_u16()
    Vr = (3.3/65535) * temperature_value
    Rt = (10000 * Vr) / (3.3 - Vr) #10000 is for 10k resistory
    temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
    Cel = temp - 273.15
    return Cel
    
def LED_on(x):
    if x >= 10:
        tenLED.value(1)
    else:
        tenLED.value(0)
    if x >= 20:
        twentyLED.value(1)
    else:
        twentyLED.value(0)
    if x >= 30:
        thirtyLED.value(1)
    else:
        thirtyLED.value(0)
    if x >= 40:
        fourtyLED.value(1)
    else:
        fourtyLED.value(0)
    if x >= 50:
        fiftyLED.value(1)
    else:
        fiftyLED.value(0)
    if x >= 60:
        sixtyLED.value(1)
    else:
        sixtyLED.value(0)
    if x >= 70:
        seventyLED.value(1)
    else:
        seventyLED.value(0)
    if x >= 80:
        eightyLED.value(1)
    else:
        eightyLED.value(0)
    if x >= 90:
        ninetyLED.value(1)
    else:
        ninetyLED.value(0)
    if x >= 100:
        hundredLED.value(1)
    else:
        hundredLED.value(0)
                
def LED_shutdown():
    tenLED.value(0)
    twentyLED.value(0)
    thirtyLED.value(0)
    fourtyLED.value(0)
    fiftyLED.value(0)
    sixtyLED.value(0)
    seventyLED.value(0)
    eightyLED.value(0)
    ninetyLED.value(0)
    hundredLED.value(0)
    
def get_color():
    url = "https://api.airtable.com/v0/appAgPl9yyloL2VGu/imageTable"
    headers = {"Authorization": "Bearer " + Token_SECRET, "Content-Type":"application/json"}
    reply = requests.get(url, headers=headers)
    if reply.status_code == 200:
        print(reply.json())
        reply = reply.json() #json array of info
        get_color = reply['records'][0]['fields']['Color']
        print(get_color)
        return get_color
    
#run farenheit for green
def fah_loop():
    while True:
        button_pushed = gamepad.digital_read()
        while button_pushed == 65575:
            client.publish("kkowalick25/feeds/i2cbutton", "ON")
            button_pushed_two = gamepad.digital_read()
            Cel = temperature_reading()
            Fah = Cel * 1.8 + 32
            print ('Celsius: %.2f C  Fahrenheit: %.2f F' % (Cel, Fah))
            LED_on(Fah)
            client.publish("kkowalick25/feeds/temperature", str(Fah))
            time.sleep(5) 
            if button_pushed_two == 65637:
                client.publish("kkowalick25/feeds/i2cbutton", "OFF")
                LED_shutdown()
                break

    #run celsius for red
def cel_loop():
    while True:
        button_pushed = gamepad.digital_read()
        while button_pushed == 65575:
            client.publish("kkowalick25/feeds/i2cbutton", "ON")
            button_pushed_two = gamepad.digital_read()
            Cel = temperature_reading()
            print ('Celsius: %.2f C' % Cel)
            LED_on(Cel)
            client.publish("kkowalick25/feeds/temperature", str(Cel))
            time.sleep(5) #change this to go every five minutes
            if button_pushed_two == 65637:
                client.publish("kkowalick25/feeds/i2cbutton", "OFF")
                LED_shutdown()
                break
            
def main():
    prev_color = ""
    cur_color = ""
    while True:
        cur_color = get_color()
        if cur_color != prev_color:
            if cur_color == "Green":
                fah_loop()
                prev_color = cur_color
            elif cur_color == "Red":
                cel_loop()
                prev_color = cur_color
        
        
main()
