#!/usr/bin/env python3
import os
import shutil
import subprocess
import urllib.request

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
        with urllib.request.urlopen(config.EARTH_URI) as res, open(config.FILE_PATH, 'wb') as f:
            shutil.copyfileobj(res, f)

    @staticmethod
    def set():
        script_dir = os.path.dirname(__file__)
        subprocess.call(["osascript", os.path.join(script_dir, "scripts/macos.scpt"), config.FILE_PATH_PNG])

    @staticmethod
    def resize():
        im = Image.open(config.FILE_PATH)

        # Resize Earth
        im.thumbnail((RESIZE_LEN, RESIZE_LEN), Image.ANTIALIAS)

        # Paste a black modal
        modal = Image.new("RGBA", (MODAL_X_LEN, MODAL_Y_LEN), (0, 0, 0, 255))
        im.paste(modal, (MODAL_X_OFFSET, MODAL_Y_OFFSET))

        # Paste Earth to a black background
        res = Image.new("RGBA", (SCREEN_X_LEN, SCREEN_Y_LEN), (0, 0, 0, 255))
        res.paste(im, (EARTH_X_OFFSET, EARTH_Y_OFFSET))

        # Save to PNG file
        res.save(config.FILE_PATH_PNG)


if __name__ == "__main__":
    Earth.get()
    Earth.resize()
    Earth.set()
