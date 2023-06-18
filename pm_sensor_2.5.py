import csv
import os
import time
from pms5003 import PMS5003
import ST7735
from PIL import Image, ImageDraw, ImageFont
from collections import deque

# Additional global variables for managing the display
last_readings = (0, 0, 0)
last_colours = (255, 255, 255)
display_update_interval = 0.1  # 10 fps
time_last_update = time.time()

# Create deque for the average change
pm25_deque = deque(maxlen=50)  # 5 seconds / 0.1 second

WIDTH, HEIGHT = 160, 80
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)
disp.begin()
font_size1 = 14
font_size2 = 36
font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size1)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size2)

def get_colour(old, new):
    if new > old:
        return (255, 0, 0)  # Red
    elif new < old:
        return (0, 255, 0)  # Green
    else:
        return (255, 255, 255)  # White

def average_pm25():
    return sum(pm25_deque) / len(pm25_deque)

def update_display(pm_2_5):
    global last_readings, last_colours, time_last_update, display_update_interval
    global pm25_deque

    now = time.time()
    if now - time_last_update >= display_update_interval:
        # Only update the display according to the desired interval (10 fps)
        time_last_update = now
        avg_pm25 = average_pm25()
        new_colour = get_colour(last_readings[1], avg_pm25)
        last_colours = new_colour
        last_readings = (0, avg_pm25, 0)

    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect_colour = (0, 180, 180)
    draw.rectangle((0, 0, 160, 80), rect_colour)

    # Text split over three lines
    draw.text((10, 5), "PM2.5", font=font1, fill=last_colours)
    draw.text((50, 20), str(pm_2_5), font=font2, fill=last_colours)
    draw.text((100, 55), "µg/m³", font=font1, fill=last_colours)

    disp.display(img)

file_number = 0
csv_file_path = f'/mnt/usb_share/pm_data_{file_number}.csv'
while os.path.isfile(csv_file_path):
    file_number += 1
    csv_file_path = f'/mnt/usb_share/pm_data_{file_number}.csv'

pms5003 = PMS5003()

header = ['Timestamp', 'PM1', 'PM2.5', 'PM10']
with open(csv_file_path, 'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)

while True:
    readings = pms5003.read()
    pm_1 = readings.pm_ug_per_m3(1)
    pm_2_5 = readings.pm_ug_per_m3(2.5)
    pm_10 = readings.pm_ug_per_m3(10)

    print(pm_1, pm_2_5, pm_10)

    timestamp = round(time.time())

    with open(csv_file_path, 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([timestamp, pm_1, pm_2_5, pm_10])

    # Update the display more frequently
    while time.time() - timestamp < 1:
        pm25_deque.append(pm_2_5)
        update_display(pm_2_5)
        time.sleep(display_update_interval)
