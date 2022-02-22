import websockets.exceptions
from fastapi import FastAPI, WebSocket, Request
from asyncio import Queue, Lock
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()


class QueueManager():
    def __init__(self):
        self.queues = []
        self.lock = Lock()

    async def add(self):
        self.queues.append(Queue())
        return self.queues[-1]

    async def remove(self, queue):
        self.queues.remove(queue)

    async def broadcast(self, data):
        async with self.lock:
            for queue in self.queues:
                await queue.put(data)


queue_manager = QueueManager()
templates = Jinja2Templates(directory='.')


@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/{width}/{height}/{color}')
async def post(width: int, height: int, color: str):
    await queue_manager.broadcast({'width': width, 'height': height, 'color': color})
    return 'OK'


@app.websocket('/feed')
async def feed(websocket: WebSocket):
    await websocket.accept()
    queue = await queue_manager.add()
    try:
        while True:
            data = await queue.get()
            await websocket.send_json(data)
    except websockets.exceptions.ConnectionClosedOK:
        pass
    finally:
        await queue_manager.remove(queue)

