from os import listdir
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import shutil
from inky.auto import auto
from starlette.responses import FileResponse

from images_in_dir import get_image_choice
from inky_utility import set_image_and_show, rotate_and_crop_image, rotate_and_resize

inky = auto()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ADJUSTED_IMAGE_DIR = "/home/pi/Pictures/adjusted/"
ORIGINAL_IMAGE_DIR = "/home/pi/Pictures/originals/"
INKY_SCREEN_RESOLUTION = inky.resolution


@app.put("/images/set/{image_name}")
def set_image(image_name: str):
    print("going to set " + image_name)
    set_image_and_show(inky, ADJUSTED_IMAGE_DIR + image_name)
    return {"message": "set " + image_name + " successfully"}


@app.put("/images/set/random/")
def set_random_image():
    image_path = get_image_choice(ADJUSTED_IMAGE_DIR)
    print("going to set " + image_path)
    set_image_and_show(inky, image_path)
    return {"message": "set " + image_path + " successfully"}


@app.put("/images/crop/{image_name}")
def crop_image_for_inky(image_name: str):
    new_name = rotate_and_crop_image(image_name, ORIGINAL_IMAGE_DIR, ADJUSTED_IMAGE_DIR)
    return {"message": "sucessfully created " + new_name}


@app.put("/images/resize/{image_name}")
def resize_image_for_inky(image_name: str):
    new_name = rotate_and_resize(image_name, ORIGINAL_IMAGE_DIR, ADJUSTED_IMAGE_DIR)
    return {"message": "sucessfully created " + new_name}


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


@app.get("/images/adjusted/")
def get_adjusted_images():
    file_list = listdir(ADJUSTED_IMAGE_DIR)
    return file_list


@app.get("/images/adjusted/get/{image_name}/download")
def get_adjusted_image_file(image_name: str):
    try:
        return FileResponse(ADJUSTED_IMAGE_DIR + image_name, media_type='application/octet-stream', filename=image_name)
    except Exception as e:
        print(e)
        return {"success": False, "reason": e.__cause__}


@app.get("/images/original/get/{image_name}/download")
def get_original_image_file(image_name: str):
    try:
        return FileResponse(ORIGINAL_IMAGE_DIR + image_name, media_type='application/octet-stream', filename=image_name)
    except Exception as e:
        print(e)
        return {"success": False, "reason": e.__cause__}

@app.get("/screen/resolution")
def get_screen_resolution():
    return inky.resolution
