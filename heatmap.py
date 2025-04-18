import os
import random
from PIL import Image, ImageDraw

# Kalibrierte Werte
a_lon = 8.763412756163602
b_lon = 1568.5272737227672
a_lat = -11.122611080927257
b_lat = 1319.0283253564514


def add_jitter(lat, lon, max_deviation=0.8):
    jitter_lat = lat + random.uniform(-max_deviation, max_deviation)
    jitter_lon = lon + random.uniform(-max_deviation, max_deviation)
    return jitter_lat, jitter_lon

def geo_to_pixel(lat, lon):
    x = a_lon * lon + b_lon
    y = a_lat * lat + b_lat
    return int(x), int(y)

def add_spot(lat, lon, color="#0693E3", radius=4):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(BASE_DIR, "static", "map.png")

    img = Image.open(IMAGE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(img)
    jlat, jlon = add_jitter(lat, lon)
    x, y = geo_to_pixel(jlat, jlon)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    img.save(IMAGE_PATH)