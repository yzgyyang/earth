import shutil
import urllib.request

import config


class Earth:
    @staticmethod
    def get_latest():
        with urllib.request.urlopen(config.EARTH_URI) as res, open(config.FILE_PATH, 'wb') as f:
            shutil.copyfileobj(res, f)


if __name__ == "__main__":
    Earth.get_latest()
