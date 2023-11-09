import numpy as np
import requests

#token removed for security purposes
Token_SECRET = ""

#initialize airTable
url = "https://api.airtable.com/v0/appAgPl9yyloL2VGu/imageTable"
headers = {"Authorization": "Bearer " + Token_SECRET, "Content-Type":"application/json"}
r=requests.get(url, headers=headers)
r.json()

#set up image
cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR)
b,g,r = cv2.split(cv2_image)

#find average value of each color 
avg_color_per_row = np.average(cv2_image, axis=0)
avg_colors = np.average(avg_color_per_row, axis=0)
print(avg_colors)

#separate array
blue = avg_colors[0]
green = avg_colors[1]
red = avg_colors[2]

#return most prevelant color
if green > red:
    print("green" + str(green))
    data = {
    "records": [
        {
            "id": "recXhDfxk4XQltDKW",
            "fields": {
                "Color": "Green"
            }
        }
    ]
}
elif red > green:
    print("red" + str(red))
    data = {
    "records": [
        {
            "id": "recXhDfxk4XQltDKW",
            "fields": {
                "Color": "Red"
            }
        }
    ]
}

response = requests.patch(url, headers=headers, json=data)
