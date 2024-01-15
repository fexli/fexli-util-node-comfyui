import re

import folder_paths  # noqa
from .utils.any_hack import any
from .categories import CATE_UTILS
from .utils.node_defs import FEAlwaysChangeNode
from copy import deepcopy
from random import Random
from .utils.lora_enc_map import FELoraEmpFinder


class FERandomLoraSelect(FEAlwaysChangeNode, FELoraEmpFinder):
    def __init__(self):
        super().__init__()
        self.random = Random()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "regex": ("STRING", {"default": "背景|style"}),
                "count": ("INT", {"default": 4, "min": 1, "max": 256, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("output",)
    FUNCTION = "roll"
    CATEGORY = CATE_UTILS
    OUTPUT_IS_LIST = (True,)

    def roll(self, regex, count, seed):
        rec = re.compile(regex, re.IGNORECASE)
        lora_list = [self.find_real_lora(_) for _ in folder_paths.get_filename_list("loras")]
        out = []
        for _ in lora_list:
            if rec.search(_):
                out.append(_)
        if len(out) < count:
            raise ValueError(f"Found {len(out)} loras matching regex '{regex}', but {count} were requested.")
        self.random = Random(seed)
        # out_lora = [self.find_current_lora(_) for _ in self.random.sample(out, count)]
        return (self.random.sample(out, count),)
