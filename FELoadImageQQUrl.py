import json
import os.path
import requests
import folder_paths  # noqa
from folder_paths import models_dir  # noqa
import comfy.sd  # noqa
import comfy.utils  # noqa
from nodes import LoraLoader  # noqa
from PIL import Image
import torch
import numpy as np

import random


def randstr(length=8):
    return ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyz', length))


class FELoadImageQQUrl:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING", {"multiline": False, }),
                "file_type": ("STRING", {"multiline": False, "default": "png"}),
                "file_unique": ("STRING", {"multiline": False, "default": ""})
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image_url"
    CATEGORY = "remote/image"
    TITLE = "Load Image (URL)"

    def load_image_url(self, url: str, file_type: str = 'png', file_unique: str = ""):
        if file_unique == "":
            file_unique = randstr(16)
        file_path_by_unique = os.path.join(folder_paths.get_input_directory(), f"{file_unique}.{file_type}")
        if not os.path.exists(file_path_by_unique):
            with open(file_path_by_unique, "wb") as f:
                f.write(requests.get(url, stream=True).raw.read())

        i = Image.open(file_path_by_unique)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
        return (image, mask)
