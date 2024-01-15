import json
import os.path

import folder_paths  # noqa
from folder_paths import models_dir  # noqa
import comfy.sd  # noqa
import comfy.utils  # noqa
from nodes import LoraLoader  # noqa
from .utils.lora_enc_map import FELoraEmpFinder


class FEEncLoraLoader(LoraLoader, FELoraEmpFinder):
    def __init__(self):
        super().__init__()
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        out_loras = [s.find_real_lora(lora) for lora in folder_paths.get_filename_list("loras")]
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_name": (out_loras,),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_lora"

    CATEGORY = "loaders"

    def load_lora(self, model, clip, lora_name, strength_model, strength_clip):
        lora_name = self.find_current_lora(lora_name)
        if not lora_name:
            return (model,clip,)
        return super().load_lora(model, clip, lora_name, strength_model, strength_clip)
