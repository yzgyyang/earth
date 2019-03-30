#!/usr/bin/env python3
import os
import shutil
import subprocess
import urllib.request

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Config
EARTH_URI = "http://rammb.cira.colostate.edu/ramsdis/online/images/latest_hi_res/himawari-8/full_disk_ahi_true_color.jpg"
DIR_PATH = os.path.expanduser("~/.earth")
DOWNLOAD_FILE = "latest.jpg"
SAVE_FILE_FORMAT = "Earth-{yyyy}{mm:0>2}{dd:0>2}-{hour:0>2}{minute:0>2}.png"
MAX_FILE_COUNT = 50
CAPTION_FORMAT = "Real-Time Earth from Himawari-8\n{yyyy}-{mm:0>2}-{dd:0>2} {hour:0>2}:{minute:0>2} Local Time"

# Constants
SCREEN_X_LEN = 2560  # Width
SCREEN_Y_LEN = 1600  # Height
RESIZE_RATIO = 0.9  # Resize Earth with respect to SCREEN_Y_LEN
MODAL_X_RATIO = 0.18  # Resize Medal with respect to RESIZE_LEN
MODAL_Y_RATIO = 0.07
CAPTION_X_RATIO = 0.81
CAPTION_Y_RATIO = 0.9
FONT_SIZE = 24

# Calculated constants
RESIZE_LEN = int(SCREEN_Y_LEN * RESIZE_RATIO)
MODAL_X_LEN = int(RESIZE_LEN * MODAL_X_RATIO)
MODAL_Y_LEN = int(RESIZE_LEN * MODAL_Y_RATIO)
MODAL_X_OFFSET = 0
MODAL_Y_OFFSET = int(RESIZE_LEN * (1 - MODAL_Y_RATIO))
EARTH_X_OFFSET = int((SCREEN_X_LEN - RESIZE_LEN) / 2)
EARTH_Y_OFFSET = int((SCREEN_Y_LEN - RESIZE_LEN) / 2)
CAPTION_X_OFFSET = int(SCREEN_X_LEN * CAPTION_X_RATIO)
CAPTION_Y_OFFSET = int(SCREEN_Y_LEN * CAPTION_Y_RATIO)


class Earth:
    def run(self):
        if self.get():
            image_path = self.resize()
            if image_path:
                self.set(image_path)

    @staticmethod
    def get():
        try:
            res = urllib.request.urlopen(EARTH_URI)
        except ConnectionResetError:
            return False
        with open(get_download_file_path(), 'wb') as f:
            shutil.copyfileobj(res, f)
        return True

    @staticmethod
    def set(file_path):
        script_dir = os.path.dirname(__file__)
        subprocess.call(["osascript", os.path.join(script_dir, "scripts/macos.scpt"), file_path])

    @staticmethod
    def resize():
        im = Image.open(get_download_file_path())

        # Resize Earth (may fail - see issue #1)
        try:
            im.thumbnail((RESIZE_LEN, RESIZE_LEN), Image.ANTIALIAS)
        except OSError:
            return None

        # Paste a black modal
        modal = Image.new("RGBA", (MODAL_X_LEN, MODAL_Y_LEN), (0, 0, 0, 255))
        im.paste(modal, (MODAL_X_OFFSET, MODAL_Y_OFFSET))

        # Paste Earth to a black background
        res = Image.new("RGBA", (SCREEN_X_LEN, SCREEN_Y_LEN), (0, 0, 0, 255))
        res.paste(im, (EARTH_X_OFFSET, EARTH_Y_OFFSET))

        # Add Caption
        script_dir = os.path.dirname(__file__)
        font = ImageFont.truetype(os.path.join(script_dir, "fonts/Heebo-Light.ttf"), FONT_SIZE)
        now = datetime.now()
        caption = CAPTION_FORMAT.format(
            yyyy=now.year, mm=now.month, dd=now.day, hour=now.hour, minute=now.minute)
        img_draw = ImageDraw.Draw(res)
        img_draw.text((CAPTION_X_OFFSET, CAPTION_Y_OFFSET), caption, font=font, fill='white')

        # Save to PNG file
        save_file_path = get_save_file_path()
        res.save(save_file_path)

        return save_file_path


def get_download_file_path():
    return os.path.join(DIR_PATH, DOWNLOAD_FILE)


def get_save_file_path():
    now = datetime.utcnow()
    save_file = SAVE_FILE_FORMAT.format(
        yyyy=now.year, mm=now.month, dd=now.day, hour=now.hour, minute=now.minute)
    return os.path.join(DIR_PATH, save_file)


def ensure_dir():
    dir_path = DIR_PATH
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def ensure_space():
    dir_path = DIR_PATH
    cur_file_count = len(os.listdir(dir_path))
    while cur_file_count >= MAX_FILE_COUNT:
        files_full_path = [os.path.join(dir_path, x) for x in os.listdir(dir_path)]
        oldest_file = min(files_full_path, key=os.path.getctime)
        os.remove(oldest_file)
        cur_file_count -= 1


if __name__ == "__main__":
    ensure_dir()
    ensure_space()
    earth = Earth()
    earth.run()
