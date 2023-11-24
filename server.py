from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from Seeker import Seeker

app = FastAPI()

seeker = Seeker()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/change_image/{item_id}")
def read_root(item_id: int):
    return {"success": item_id}

@app.get("/get_count")
def read_root():
    return {"count": seeker.count()}