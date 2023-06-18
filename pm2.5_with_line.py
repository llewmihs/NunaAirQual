import csv
import os
import time
from collections import deque
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

# Deque for storing PM2.5 data for the line graph
graph_data = deque(maxlen=WIDTH - 40)  # Store only the latest data points to fit the screen width

# Function to draw line graph
def draw_line_graph(draw, data, y_max=50, y_min=0):
    y_range = y_max - y_min
    x_step = (WIDTH - 40) // max(1, len(data) - 1)
    for i in range(1, len(data)):
        x1 = (i - 1) * x_step + 40
        x2 = i * x_step + 40
        y1 = HEIGHT - HEIGHT * (data[i - 1] - y_min) / y_range
        y2 = HEIGHT - HEIGHT * (data[i] - y_min) / y_range
        draw.line([(x1, y1), (x2, y2)], fill=colour)

# Function to update display
def update_display(pm_2_5):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect_colour = (0, 180, 180)
    draw.rectangle((0, 0, 160, 80), rect_colour)

    text = f"PM 2.5: {pm_2_5} µg/m³"
    draw.text((0, 0), text, font=font, fill=colour)

    draw_line_graph(draw, graph_data)
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
    graph_data.append(pm_2_5)
    update_display(pm_2_5)

    timestamp = round(time.time())

    with open(csv_file_path, 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([timestamp, pm_1, pm_2_5, pm_10])

    time.sleep(5)
