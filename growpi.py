import csv
import math
import os
import picamera
import secrets
import time

from ftplib import FTP
from grovepi import *
from sleepto import *

# Connect the Grove Moisture Sensor to analog port A0, Light Sensor to A1
# Connect Red Led to D3, DHT22 Sensor to D4

# Sensors
moistureSensor = 0
lightSensor = 1
ledRed = 3
tempSensor = 4

loopInterval = 10  # How many minutes until next interval
lightThreshold = 10  # Value above threshold is lightsOn

localImagePath = '/home/pi/Desktop/images/'  # Where the images are stored


# Write data to csv
def appendCSV():
    fields = ['Time', 'Temperature', 'Humidity', 'Moisture', 'MoistureClass',
              'Light', 'LightsOn', 'PiTemperature', 'Image', 'WaterGiven']
    with open(r'temp.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow({'Time': currentTime,
                         'Temperature': temp,
                         'Humidity': humidity,
                         'Moisture': moisture,
                         'MoistureClass': moistureClass,
                         'Light': lightValue,
                         'LightsOn': lightsOn,
                         'PiTemperature': (piTemperature()),
                         'Image': image,
                         'WaterGiven': 0
                         })


def moistureClassifier():
    if moisture < 300:
        moistureResult = 'Dry'
    elif moisture < 600:
        moistureResult = 'Moist'
    else:
        moistureResult = 'Wet'
    return moistureResult


def piTemperature():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp[5:9]


def printSensorData():
    print(currentTime)
    if math.isnan(temp) == False and math.isnan(humidity) == False:
        print("Temperature: {}'C\nHumidity: {}%".format(temp, humidity))
    else:
        print("Couldn't get temperature/humidity sensor readings")
    print('Moisture: {0} ({1})'.format(moisture, moistureClass))
    print("Lights: {} ({})".format(lightValue, "On" if lightsOn else "Off"))
    print("Raspberry pi: {}'C".format(piTemperature()))
    if lightsOn:
        print("Image: {}\n".format(image))
    else:
        print("")


def takePicture():
    timestamp = time.strftime("%Y-%m-%d--%H-%M")
    image = '{}.jpg'.format(timestamp)
    imagePath = localImagePath + image
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.awb_mode = 'sunlight'
        time.sleep(5)
        camera.capture(imagePath)
        camera.stop_preview()
    return image


def uploadCSV():
    ftp = FTP(secrets.FTP_URL)
    ftp.login(user=secrets.USERNAME, passwd=secrets.PASSWORD)
    filename = 'temp.csv'
    ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
    ftp.quit()


def uploadImage():
    if image:
        ftp = FTP(secrets.FTP_URL)
        ftp.login(user=secrets.USERNAME, passwd=secrets.PASSWORD)
        ftp.cwd('/images/')
        filename = localImagePath + image
        ftp.storbinary('STOR ' + image, open(filename, 'rb'))
        ftp.quit()


while True:
    try:
        # Start loop at every loopInterval minute of the hour
        SleepTo.nextMinuteInterval(loopInterval)
        # Get sensor readings
        lightValue = analogRead(lightSensor)
        moisture = analogRead(moistureSensor)
        [temp, humidity] = dht(tempSensor, 1)

        currentTime = time.ctime()
        moistureClass = moistureClassifier()
        lightsOn = lightValue > lightThreshold

        # Lights on
        if lightsOn:
            # Turn on red LED when ground is dry and append moisture to waterCheck
            if moistureClass == 'Dry':
                digitalWrite(ledRed, 1)

            # Ground not Dry
            else:
                digitalWrite(ledRed, 0)

            # Take picture every loop, while lightsOn, store path in image variable
            image = takePicture()

            # PrintSensorData, appendCSV, UploadImage and CSV
            printSensorData()
            appendCSV()
            uploadImage()
            uploadCSV()

        # Lights off
        else:
            # In case ground was dry, when lightsOn
            digitalWrite(ledRed, 0)

            # No picture when lights off, empty string for appendCSV
            image = ''

            printSensorData()
            appendCSV()
            uploadCSV()

    except KeyboardInterrupt:
        digitalWrite(ledRed, 0)
        print(" Shutdown safely")
        break
    except IOError:
        print("Error")
