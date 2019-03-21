#!/usr/bin/env python3
import os
import shutil
import subprocess
import urllib.request

import config


class Earth:
    @staticmethod
    def get_latest():
        with urllib.request.urlopen(config.EARTH_URI) as res, open(config.FILE_PATH, 'wb') as f:
            shutil.copyfileobj(res, f)

    @staticmethod
    def set():
        script_dir = os.path.dirname(__file__)
        subprocess.call(["osascript", os.path.join(script_dir, "scripts/macos.scpt"), config.FILE_PATH])


if __name__ == "__main__":
    Earth.get_latest()
    Earth.set()
