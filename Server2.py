import asyncio
from threading import Thread

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

from Seeker import Seeker
from Camera import Cam

app = FastAPI()


def ask():
    seeker.model_work(camera.parse(), crop=crops[modes[mode] - 1])


@app.get("/{c_mode}/{image_or_count}")
async def change_mode(c_mode: str, image_or_count: str):
    global mode, camera
    if c_mode != mode:
        if c_mode.isdigit():
            mode = {item: key for key, item in modes.values()}[int(c_mode)]
        else:
            mode = c_mode
        camera = Cam(path=f"video/vid_{modes[mode]}.mp4")
        ask()
    else:
        ask()
    if image_or_count != "count":
        path = Path(f"res.jpg")
        return FileResponse(path)
    return {"count": seeker.count}

if __name__ == '__main__':
    import uvicorn

    image = 1
    seeker = Seeker()
    mode = "queue"
    modes = {"queue": 1, "hall": 2}
    l0 = (310, 50, 780, 540)
    l1 = (0, 0, 640, 720)
    crops = [l0, l1]
    camera = Cam(path=f"video/vid_{modes[mode]}.mp4")
    uvicorn.run(app, host="127.0.0.1", port=8001)
