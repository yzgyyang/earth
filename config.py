import os

EARTH_URI = "http://rammb.cira.colostate.edu/ramsdis/online/images/latest_hi_res/himawari-8/full_disk_ahi_true_color.jpg"
DIR_PATH = os.path.expanduser("~/.earth")
DOWNLOAD_FILE = "latest.jpg"
SAVE_FILE_FORMAT = "Earth-{yyyy}{mm:0>2}{dd:0>2}-{hour:0>2}{minute:0>2}.png"
MAX_FILE_COUNT = 50
