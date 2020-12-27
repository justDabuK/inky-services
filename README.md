# Requirements
If pi Zero W, then one first need to setup Wifi on another PI.
And before that, allowing SSH by putting file with the name 
`SSH` into the root directory of the SD-Card.

Inky, Python 3, FastAPI, Uvicorn

    curl https://get.pimoroni.com/inky | bash
    pip3 install fastapi
    pip3 install uvicorn
    pip3 install python-multipart


# cronjobs

    @reboot /home/pi/.local/bin/uvicorn --app-dir /home/pi/workspace/ --host 0.0.0.0 inky_service:app > /home/pi/logs/inky_service.logs 2>&1
    0 *  *   *   *     python3 /home/pi/workspace/set_random_image.py /home/pi/Pictures/adjusted/

# files system adjustments
- `~/logs` directory for the inky_service
- `~/Pictures/originals` and `~/Pictures/adjusted` with pictures 
