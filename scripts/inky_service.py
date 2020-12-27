from os import listdir
from fastapi import FastAPI, File, UploadFile
import shutil
from PIL import Image
from inky.inky_uc8159 import Inky
from images_in_dir import get_image_choice
from inky_utility import set_image_and_show

inky = Inky()

app = FastAPI()

ADJUSTED_IMAGE_DIR = "/home/pi/Pictures/adjusted/"
ORIGINAL_IMAGE_DIR = "/home/pi/Pictures/originals/"
INKY_SCREEN_RESOLUTION = (600, 448)


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
def rotate_and_crop_image(image_name: str):
    image_path = ORIGINAL_IMAGE_DIR + image_name
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    size = rotated_image.size
    box = (
        size[0] / 2 - INKY_SCREEN_RESOLUTION[0] / 2,
        size[1] / 2 - INKY_SCREEN_RESOLUTION[1] / 2,
        size[0] / 2 + INKY_SCREEN_RESOLUTION[0] / 2,
        size[1] / 2 + INKY_SCREEN_RESOLUTION[1] / 2
    )
    smaller_rotated_image = rotated_image.crop(box)
    image_name_split = image_name.split('.')
    smaller_rotated_image.save(ADJUSTED_IMAGE_DIR + image_name_split[0] + '_cropped_rotated.' + image_name_split[1])
    return {"message": "sucessfully created " + image_name_split[0] + '_cropped_rotated.' + image_name_split[1]}


@app.put("/images/resize/{image_name}")
def rotate_and_crop_image(image_name: str):
    image_path = ORIGINAL_IMAGE_DIR + image_name
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    smaller_rotated_image = rotated_image.resize(INKY_SCREEN_RESOLUTION)
    image_name_split = image_path.split('.')
    smaller_rotated_image.save(ADJUSTED_IMAGE_DIR + image_name_split[0] + '_resized_rotated.' + image_name_split[1])
    return {"message": "sucessfully created " + image_name_split[0] + '_resized_rotated.' + image_name_split[1]}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if "image" in file.content_type:
        with open(ORIGINAL_IMAGE_DIR + file.filename, "wb") as local_file:
            shutil.copyfileobj(file.file, local_file)
        return {"success": True}
    else:
        return {"success": False, "reason": "wrong type: " + file.content_type}


@app.get("/images/original/")
def get_images():
    file_list = listdir(ORIGINAL_IMAGE_DIR)
    return file_list


@app.get("/images/adjusted/")
def get_images():
    file_list = listdir(ADJUSTED_IMAGE_DIR)
    return file_list
