from PIL import Image
import requests
from multiprocessing import Pool
import random

def rgb2hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)

with Image.open('img.png') as img:
    pixels = img.resize((400, 300)).convert('RGB')

    s = requests.Session()

    def f(z):
        x, y = z
        s.post(f'http://10.1.0.198:8000/{x}/{y}/{rgb2hex(*pixels.getpixel((x, y)))}')

    l = [(x, y) for x in range(400) for y in range(300)]

    random.shuffle(l)

    with Pool(30) as p:
        p.map(f, l)