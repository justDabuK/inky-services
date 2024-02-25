from os import listdir, path
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

import shutil
from inky.auto import auto
from starlette.responses import FileResponse
from typing import List

from images_in_dir import get_image_choice
from inky_utility import set_image_from_path_and_show, adjust_image

inky = auto()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ORIGINAL_IMAGE_DIR = "/home/pi/Pictures/originals/"
CURRENT_IMAGE_DIR = "/home/pi/Pictures/current/"
INKY_SCREEN_RESOLUTION = inky.resolution


@app.put("/images/set/{image_name}")
def set_image(image_name: str):
    print("going to set " + image_name)
    set_image_from_path_and_show(inky, ORIGINAL_IMAGE_DIR + image_name)
    return {"message": "set " + image_name + " successfully"}


@app.put("/images/set/random/")
def set_random_image():
    image_path = get_image_choice(ORIGINAL_IMAGE_DIR)
    print("going to set " + image_path)
    set_image_from_path_and_show(inky, image_path)
    return {"message": "set " + image_path + " successfully"}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if "image" in file.content_type:
        with open(ORIGINAL_IMAGE_DIR + file.filename, "wb") as local_file:
            shutil.copyfileobj(file.file, local_file)
        return {"success": True}
    else:
        return {"success": False, "reason": "wrong type: " + file.content_type}


@app.get("/images/original/")
def get_original_images():
    file_list = listdir(ORIGINAL_IMAGE_DIR)
    return file_list


@app.get("/images/original/get/{image_name}/download")
def get_original_image_file(image_name: str):
    try:
        return FileResponse(ORIGINAL_IMAGE_DIR + image_name, media_type='application/octet-stream', filename=image_name)
    except Exception as e:
        print(e)
        return {"success": False, "reason": e.__cause__}


@app.put("/images/current/get/download")
def get_current_image(resolution: List[int]):
    try:
        is_current_file_png = path.exists(CURRENT_IMAGE_DIR + "current.png")
        is_current_file_jpg = path.exists(CURRENT_IMAGE_DIR + "current.jpg")
        is_current_file_jpeg_with_e = path.exists(CURRENT_IMAGE_DIR + "current.jpeg")

        file_ending = ""
        if is_current_file_png:
            file_ending = "png"
        elif is_current_file_jpg:
            file_ending = "jpg"
        elif is_current_file_jpeg_with_e:
            file_ending = "jpeg"
        else:
            return {"success": False, "reason": "no current image found"}

        desired_image_path = f"{CURRENT_IMAGE_DIR}current_{resolution[0]}_{resolution[1]}.{file_ending}"
        if not path.exists(desired_image_path):
            current_image = adjust_image(f"{CURRENT_IMAGE_DIR}current.{file_ending}", resolution)
            current_image.save(f"{CURRENT_IMAGE_DIR}current_{resolution[0]}_{resolution[1]}.{file_ending}")

        return FileResponse(desired_image_path, media_type=f"image/{file_ending}")
    except Exception as e:
        print(e)
        return {"success": False, "reason": e.__cause__}


@app.get("/screen/resolution")
def get_screen_resolution():
    return inky.resolution
