import paho.mqtt.client as mqtt
import requests
     
#airtable and adafruit information (removed for security)
Token_ID = ""
Token_SECRET = ""
adafruit_USER = ""
adafruit_KEY = ""
    
#connect to Adafruit Dashboard (does this even need to occur)
url = 'https://io.adafruit.com/api/v2/%s/feeds' % adafruit_USER
headers = {'X-AIO-Key':adafruit_KEY,'Content-Type':'application/json'}
print(headers)
print(url)
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

client = mqtt.Client("KellisPC")
client.username_pw_set(adafruit_USER, adafruit_KEY)
client.connect("io.adafruit.com", 1883, keepalive=600)

#get color from airtable and send it to adafruit
while True:
    url = "https://api.airtable.com/v0/appAgPl9yyloL2VGu/imageTable"
    headers = {"Authorization": "Bearer " + Token_SECRET, "Content-Type":"application/json"}
    reply = requests.get(url, headers=headers)
    if reply.status_code == 200:
        print(reply.json())
        reply = reply.json() #json array of info
        get_color = reply['records'][0]['fields']['Color']
        print(get_color)
    if get_color == "Red":
        print("Celsius")
        client.publish("kkowalick25/feeds/cel-slash-fah", "°C")
    elif get_color == "Green":
        print("Farenheit")
        client.publish("kkowalick25/feeds/cel-slash-fah", "°F")

client.loop_forever()
