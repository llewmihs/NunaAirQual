import csv
import os
import time
from pms5003 import PMS5003
import ST7735
from PIL import Image, ImageDraw, ImageFont

# Display setup
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
font_size = 18
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
colour = (255, 255, 255)

# Create a function to update display
def update_display(pm_1, pm_2_5, pm_10):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect_colour = (0, 180, 180)
    draw.rectangle((0, 0, 160, 80), rect_colour)

    text = f"PM 1: {pm_1} µg/m³\nPM 2.5: {pm_2_5} µg/m³\nPM 10: {pm_10} µg/m³"
    draw.text((0, 0), text, font=font, fill=colour)

    disp.display(img)

# Rest of the code is unchanged
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
    update_display(pm_1, pm_2_5, pm_10)

    timestamp = round(time.time())

    with open(csv_file_path, 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([timestamp, pm_1, pm_2_5, pm_10])

    time.sleep(1)
