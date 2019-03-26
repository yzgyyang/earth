# Earth

Make Earth your real time wallpaper!

![Sample Screenshot](https://user-images.githubusercontent.com/16748524/54847076-a6493180-4c9a-11e9-9a5b-d1393e705902.JPG)

## Supported Platform

macOS Mojave (Tested)

## Installation

```
brew install python3
pip3 install Pillow
```

Add a crontab:
```
crontab -e
# Write to file
*/10 * * * * /usr/local/bin/python3 <path/to/repo>/earth.py
```
