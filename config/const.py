#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from .conf import BASE_DIR

DOWNLOAD_PATH = "download"
COLOR_PATH = "download/color"

download_path = os.path.join(BASE_DIR, DOWNLOAD_PATH)
os.makedirs(download_path, exist_ok=True)
color_path = os.path.join(BASE_DIR, COLOR_PATH)
os.makedirs(color_path, exist_ok=True)

