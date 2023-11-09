# roboticsMidterm
A project to build a thermometer with physical and virtual output of temperature. This project converts readings from a thermistor to temperature readings and outputs them into a ten LED thermometer as well as an Adafruit Dashboard.  

To implement the project, the four following scripts are needed:

PyScript:
  This program is responsible for the image processing aspect. It takes in an image snapshot and determines the color of the largest object in the image between red and green. 
  From there it, posts the information to the color to Airtable in the imageTable using RestAPI.
  
  The code from this file can copied to replace the code in the REPL of the following link [and](https://chrisrogers.pyscriptapps.com/me35-midterm/latest/). An image must first be 
  taken and then the code can be run using control return. 

gamepad.py:
  This is a library used to read in movements on the gamepad written by Phila and Jordan during the "Talking in Sentences" project. This script also requires the additional 
  libraries of machine, struct, and time.
  
  To use the library, it must first be installed on the pico, then imported to the micropython script. From there the gamepad must be initialized using the gamepad.digital_setup() 
  function to enable further use.

roboticsMidtermPC.py:
  This script is run on python3 and requires the installation of the paho-mqtt and requests libraries. This program reads in the color off of the Airtable record using RestAPI and 
  switches the Celsius/Farenheit switch on the Adafruit Dashboard accordingly using MQTT.

roboticsMidtermPico.py
  This script is run on micropython and requires the installation of mqtt, requests, machine, math, time, and gamepad. This program begins outputting temperature readings when 
  the "X" button is pushed on the gamepad, outputting them to the Adafruit Dashboard through MQTT and displaying them in the LEDS of the physical thermometer. The readings and 
  LEDS shutdown when the "B" button is pushed. The program outputs these readings in celsius or farenheit dependent on the color it reads in from the Airtable through RestAPI. The
  program also toggles an on and off switch on the Adafruit Dashboard when the "X" and "B" buttons are pressed. 

NOTE: In order to run the following to scripts at the same time, they must be run on different applications since one is run on micropython and one is run on python3. My 
suggestion would be to use VScode to run the python script and Thonny for the micropython script.

An Adafruit Dashboard and Airtable are also required for these programs to run correctly. The usernames and passwords (keys/tokens,etc.) used for these sites should be your own 
and kept secret when sharing the code with others. The code should also be modified to fit the specfic feed names chosen on Adafruit as well as the IDs of the Airtable for your 
specific sites. 

Special thanks to:
  SunFounder (https://docs.sunfounder.com/projects/thales-kit/en/latest/micropython/thermometer.html) for code on converting thermistor resistance values to temperature values.
  https://www.timpoulsen.com/2018/finding-the-dominant-colors-of-an-image.html for code on how to get the average values of colors within an image.
  
