from os import listdir
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

import shutil

app = FastAPI()

IMAGE_DIR = "/Users/k.just/workspace/muddi/pictures/"


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if "image" in file.content_type:
        with open(IMAGE_DIR + file.filename, "wb") as local_file:
            shutil.copyfileobj(file.file, local_file)
        return {"success": True}
    else:
        return {"success": False, "reason": "wrong type: " + file.content_type}


@app.get("/images/")
def get_images():
    file_list = listdir(IMAGE_DIR)
    return file_list


@app.put("/images/set/{image_name}")
def set_image(image_name: str):
    return {"image_name": image_name}
