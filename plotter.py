import random

import websocket
from PIL import Image
from tqdm import tqdm
from websocket import create_connection


def rgb2hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


with Image.open('java-logo-vector.png') as img:
    pixels = img.resize((400, 300)).convert('RGB')

    l = [(x, y) for x in range(400) for y in range(300)]

    print(len(l))
    random.shuffle(l)

    ws: websocket.WebSocket = create_connection('ws://10.1.0.198:8000/set_pixel')
    ws.settimeout = 1

    j = 1
    for i in tqdm(l):
        x, y = i
        # sleep(0.00001)
        r, g, b = pixels.getpixel((x, y))
        # r, g, b = 0, 0, 0
        ws.send(f'{x} {y} {r} {g} {b}')
        j += 1
        if j % 30000 == 0:
            _ = [ws.recv() for _ in range(30000 - 1)]
            j = 1
        # _data = ws.recv_data()

    ws.close(timeout=10)
