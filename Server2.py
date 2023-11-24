import asyncio
from threading import Thread

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

from Seeker import Seeker
from Camera import Cam

app = FastAPI()

image = 1
seeker = Seeker()
camera = Cam()
Tr


@app.get("/change_image/{item_id}")
async def read_root(item_id: int):
    global image
    image = item_id.__int__()
    print(image)
    seeker.model_work(f"images/{image}.jpg")
    return {"success": item_id}


@app.get("/get_count")
async def count():
    return {"count": seeker.count}


@app.get("/get_image")
async def image():
    path = Path(f"res.jpg")
    return FileResponse(path)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
