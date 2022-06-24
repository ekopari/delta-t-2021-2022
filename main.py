from datetime import datetime , timedelta
from time import sleep
from pathlib import Path
from sense_hat import SenseHat
from gpiozero import MotionSensor
from orbit import ISS
from skyfield.api import load
from picamera import PiCamera
import led_messages
import cv2
import numpy as np
import csv

base_folder = Path(__file__).parent.resolve()
measurements_file = base_folder / "data.csv"

resolution = (1312,976)
picture = np.empty((resolution[1] , resolution[0] , 3) , dtype=np.uint8)
histogram_file = base_folder / "histograms.bin"

with open(measurements_file , 'w', buffering=1) as f:
    writer = csv.writer (f)
    header = ("Date/time" , "Temperature" , "Humidity","Pressure" ,"accel x","accel y ", "accel z","gyro x" , "gyro y","gyro z" ,"compass x" ,"compass y" , "compass z", "pir_motion","color blue","color red","color green","color clear","color gain","latitude","longitude","elevation")
    writer.writerow(header)

camera = PiCamera()
camera.resolution = resolution
camera.start_preview()

sense = SenseHat()
sense.rotation = 270
sense.clear()

led_messages.sense = sense
led_messages.start_loop()

pir = MotionSensor(pin=12)

start_time = datetime.now()
end_time = start_time + timedelta(minutes=178)

sense.color.gain = 1
sense.color.integration_cycles = 64

gain_values = [1 , 4 , 16 , 60]

#automatically setting the correct light sensor gain
def rgbc():
    for gain_value in gain_values:
        sense.color.gain = gain_value
        sleep(2 * sense.color.integration_time)
        red, green, blue, clear = sense.colour.colour
        if clear>35:
            break
    return sense.colour.colour

sleep(2)
while datetime.now()<end_time:
    red, green, blue, clear = rgbc()
    gain = sense.color.gain
    
    camera.capture(picture , "bgr")
    blueChannel, greenChannel, redChannel = cv2.split(picture)
    histogram_b = cv2.calcHist([blueChannel] , [0] , None , [256] , [0,256])
    histogram_g = cv2.calcHist([greenChannel] , [0] , None , [256] , [0,256])
    histogram_r = cv2.calcHist([redChannel] , [0] , None , [256] , [0,256])
    
    timeISSposition = load.timescale().now()
    position = ISS.at(timeISSposition)
    location = position.subpoint()
    temperature = sense.temperature
    humidity = sense.humidity
    pressure = sense.pressure
    acceleration =sense.get_accelerometer_raw()
    gyro= sense.get_gyroscope_raw()
    compass = sense.get_compass_raw()
    pir_motion = pir.value
    with open(measurements_file, 'a', buffering=1) as f:
        writer = csv.writer(f)
        row = (datetime.now() , temperature , humidity, pressure ,acceleration["x"],acceleration["y"],acceleration["z"],gyro["x"],gyro["y"],gyro["z"],compass["x"],compass["y"],compass["z"],pir_motion, blue, red, green, clear, gain, location.latitude,location.longitude,location.elevation.km)
        writer.writerow(row)
    with open(histogram_file , 'ab') as f:
        f.write(histogram_b.tobytes())
        f.write(histogram_g.tobytes())
        f.write(histogram_r.tobytes())
    sleep(3)

led_messages.stop_loop()
