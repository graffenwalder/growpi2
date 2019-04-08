# growPi - V2

Raspberry pi, with GrovePi+ to read plant data. Data is saved to `temp.csv`. Takes a picture on every interval.
If moisture readings are "Dry" for 5 consecutive intervals, the water pump will activate.

Sensors: moisture, light, temperature and humidity.

![growPi](/images/plantsense.jpg)

## Hardware

- Raspberry Pi 3B+
  - Adapter
  - 32GB SD Card (8GB is enough when not using camera)
- GrovePi+
  - [Moisture Sensor](http://wiki.seeedstudio.com/Grove-Moisture_Sensor/)
  - [Light Sensor](http://wiki.seeedstudio.com/Grove-Light_Sensor/)
  - [LED Red (5mm)](http://wiki.seeedstudio.com/Grove-Red_LED/)
  - [Temperature & Humidity Sensor (DHT22)](http://wiki.seeedstudio.com/Grove-Temperature_and_Humidity_Sensor_Pro/)
  - [Mini Fan](http://wiki.seeedstudio.com/Grove-Mini_Fan/)
- [3-6V Waterpump](https://www.bitsandparts.eu/Motoren-Servos-and-Drivers/Doseringspomp-Waterpomp-dompelpomp-3-6V-120l-h/p116339)
  - Aquarium tubing
  - Water container (bottle, bucket.....)
  - 2 female to female jumper wires
- Optional:
  - Heat sink for Raspberry Pi
  - Raspberry Pi Camera (Board V2 - 8MP)

## Setup

1. Download and burn [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) to SD card.
2. Do initial Raspbian setup, make sure to setup an internet connection.
3. Update Raspbian:
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get dist-upgrade
```
4. Attach GrovePi+ To Raspberry Pi and run:
```
$ sudo curl -kL dexterindustries.com/update_grovepi | bash
$ sudo reboot
```
5. After reboot run:
```
$ sudo i2cdetect -y 1
```
- If the install was successful, you should see "04" in the output.
- See [GrovePi Setup](https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/) if unsuccessful.
6. Connect water pump to Mini Fan board:
- Carefully take off the plastic shell of both the jumper wires, on one end.
- Pull the water pump wires through the small holes of the shells.
- Put the water pump wires in the stripped opening of the jumper wires and attach them with some pliers
- Pull back the shells.
- Attach the other end of the jumper wires to the Mini Fan board, where the Mini Fan plug normally goes.
- Attach aquarium tubing and put in water container.
![waterpump](/images/waterpump.jpg)
7. Connect sensors to the GrovePi ports:

| Module/Sensor                  | Port  |
| -------------------------------|-------|
| Moisture Sensor                | A0    |
| Light Sensor                   | A1    |
| Mini Fan board (water pump)	 | D2	 |
| LED Red                        | D3    |
| Temperature & Humidity Sensor  | D4    |

Feel free to use different ports, just be sure to change them in `growpi.py`.

## Website Setup
![website screenshot](/images/webscreenshot.jpg)

8. Open `secrets.py`, and fill out your ftp url, username and password:
```
FTP_URL = 'ftp.example.com'
USERNAME = 'your_username'
PASSWORD = '123456'
```
9. Copy the contents of the website directory, to the root of your website.
10. Launch growPi:
```
$ python growpi.py
```

## ToDoList

- [x] Base script
- [x] Add Sensors: Moisture, Temperature, Humidity, Light
- [x] Add red led as indicator for low moisture
- [x] Save sensor data to csv file
- [x] Add camera
- [x] Add water pump
- [x] Write watering logic
- [x] Write water pump setup
- [x] Make Web app/site that auto updates with sensor data
- [ ] Add Jupyter notebook with EDA if interesting

## Notes

- The water pump in this setup produces about 5ml/second. Make sure to test how much your setup produces, results may vary.
- If you don't want to use the website, just remove all `uploadCSV()` and `UploadImage()` function calls from the main loop.
- If you want to get the timelapse video, download `timelapse.py` and `secrets.py`, and run `timelapse.py` on your local machine.
Or upload them to a server and add `timelapse.py` to a cronjob, so the video will get updated automatically.
