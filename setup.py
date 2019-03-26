#!/usr/bin/env python3
from setuptools import setup

with open("requirements.txt") as requirements:
    install_requires = requirements.read().splitlines()

if __name__ == "__main__":
    setup(name="earth",
          version="0.1",
          description="Make Earth your real time wallpaper",
          license="BSD-3-Clause",
          author="Guangyuan Yang",
          author_email="yzgyyang@outlook.com",
          install_requires=install_requires)
