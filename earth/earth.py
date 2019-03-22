#!/usr/bin/env python3
import os
import shutil
import subprocess
import urllib.request

from datetime import datetime
from PIL import Image

import config


# Constants
SCREEN_X_LEN = 2560  # Width
SCREEN_Y_LEN = 1600  # Height
RESIZE_RATIO = 0.9  # Resize Earth with respect to SCREEN_Y_LEN
MODAL_X_RATIO = 0.18  # Resize Medal with respect to RESIZE_LEN
MODAL_Y_RATIO = 0.07

# Calculated constants
RESIZE_LEN = int(SCREEN_Y_LEN * RESIZE_RATIO)
MODAL_X_LEN = int(RESIZE_LEN * MODAL_X_RATIO)
MODAL_Y_LEN = int(RESIZE_LEN * MODAL_Y_RATIO)
MODAL_X_OFFSET = 0
MODAL_Y_OFFSET = int(RESIZE_LEN * (1 - MODAL_Y_RATIO))
EARTH_X_OFFSET = int((SCREEN_X_LEN - RESIZE_LEN) / 2)
EARTH_Y_OFFSET = int((SCREEN_Y_LEN - RESIZE_LEN) / 2)


class Earth:
    @staticmethod
    def get():
        with urllib.request.urlopen(config.EARTH_URI) as res, open(get_download_file_path(), 'wb') as f:
            shutil.copyfileobj(res, f)

    @staticmethod
    def set(file_path):
        script_dir = os.path.dirname(__file__)
        subprocess.call(["osascript", os.path.join(script_dir, "scripts/macos.scpt"), file_path])

    @staticmethod
    def resize():
        im = Image.open(get_download_file_path())

        # Resize Earth
        im.thumbnail((RESIZE_LEN, RESIZE_LEN), Image.ANTIALIAS)

        # Paste a black modal
        modal = Image.new("RGBA", (MODAL_X_LEN, MODAL_Y_LEN), (0, 0, 0, 255))
        im.paste(modal, (MODAL_X_OFFSET, MODAL_Y_OFFSET))

        # Paste Earth to a black background
        res = Image.new("RGBA", (SCREEN_X_LEN, SCREEN_Y_LEN), (0, 0, 0, 255))
        res.paste(im, (EARTH_X_OFFSET, EARTH_Y_OFFSET))

        # Save to PNG file
        save_file_path = get_save_file_path()
        res.save(save_file_path)

        return save_file_path


def get_download_file_path():
    return os.path.join(config.DIR_PATH, config.DOWNLOAD_FILE)


def get_save_file_path():
    now = datetime.utcnow()
    save_file = config.SAVE_FILE_FORMAT.format(
        yyyy=now.year, mm=now.month, dd=now.day, hour=now.hour, minute=now.minute)
    return os.path.join(config.DIR_PATH, save_file)


def ensure_dir():
    dir_path = config.DIR_PATH
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def ensure_space():
    dir_path = config.DIR_PATH
    cur_file_count = len(os.listdir(dir_path))
    while cur_file_count >= config.MAX_FILE_COUNT:
        files_full_path = [os.path.join(dir_path, x) for x in os.listdir(dir_path)]
        oldest_file = min(files_full_path, key=os.path.getctime)
        os.remove(oldest_file)
        cur_file_count -= 1


if __name__ == "__main__":
    ensure_dir()
    ensure_space()
    Earth.get()
    Earth.set(Earth.resize())
