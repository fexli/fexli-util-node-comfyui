import hashlib

import folder_paths  # noqa # as-root
from comfy.cli_args import args  # noqa # as-root

from PIL import Image, ImageOps
from PIL.PngImagePlugin import PngInfo
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from .categories import CATE_IMAGE
from io import BytesIO
import numpy as np
import json
import os


class FESaveEncryptImage:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "CCUI"}),
                "password": ("STRING", {"default": ""}),
                "erase_pwd_in_meta": (["yes", "no"], {"default": "yes"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = CATE_IMAGE

    def erase_pwd(self, inp, pwd):
        return inp.replace(pwd, "********")

    def save_images(self, images, filename_prefix="CCUI", password="", erase_pwd_in_meta="yes", prompt=None,
                    extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                dumppwd = json.dumps(password)[1:-1]
                if prompt is not None:
                    ppr_ = json.dumps(prompt)
                    if erase_pwd_in_meta == "yes" and password:
                        ppr_ = self.erase_pwd(ppr_, dumppwd)
                    metadata.add_text("prompt", ppr_)
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        ppr_ = json.dumps(extra_pnginfo[x])
                        if erase_pwd_in_meta == "yes" and password:
                            ppr_ = self.erase_pwd(ppr_, dumppwd)
                        metadata.add_text(x, ppr_)
            if password:
                file = f"{filename}_{counter:05}_.epng"
                imgio = BytesIO()
                img.save(imgio, "PNG", pnginfo=metadata, compress_level=4)

                key = hashlib.sha256(password.encode("utf-8")).digest()
                iv = get_random_bytes(16)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                cipher_text = cipher.encrypt(pad(imgio.getvalue(), AES.block_size))
                outio = BytesIO()
                outio.write(b"EPNG")
                outio.write(cipher_text)
                outio.write(iv)

                with open(os.path.join(full_output_folder, file), "wb") as f:
                    f.write(outio.getvalue())
                results.append({
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type
                })
            else:
                file = f"{filename}_{counter:05}_.png"
                img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=4)
                results.append({
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type
                })
            counter += 1

        return {"ui": {"images": results}}
