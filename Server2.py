from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

from Seeker import Seeker
from Camera import Cam

app = FastAPI()

image = 1
seeker = Seeker()
camera = Cam()


@app.get("/get_count")
async def count():
    seeker.model_work(camera.parse())
    return {"count": seeker.count}


@app.get("/get_image")
async def image():
    seeker.model_work(camera.parse())
    path = Path(f"res.jpg")
    return FileResponse(path)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
