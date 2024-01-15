import os

from .categories import CATE_UTILS
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode
from random import Random

base_node_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FERandomPrompt(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "read_from": ("STRING", {"default": "ComfyUI-Custom-Scripts/user/autocomplete.txt"}),
                "count": ("INT", {"default": 1, "min": 0, "max": 75}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('output',)
    FUNCTION = "get_rand"
    SAVED_PROMPTS = []
    FILE_MDATE = 0
    random_inst = Random()

    OUTPUT_NODE = True

    CATEGORY = CATE_UTILS

    def get_rand(self, read_from, count, seed):
        if os.stat(os.path.join(base_node_folder, read_from)).st_mtime != self.FILE_MDATE:
            self.FILE_MDATE = os.stat(os.path.join(base_node_folder, read_from)).st_mtime
            self.SAVED_PROMPTS = []
            with open(os.path.join(base_node_folder, read_from), 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    self.SAVED_PROMPTS.append(line.strip().rsplit(',', 1)[0])
        assert count <= len(self.SAVED_PROMPTS), "count too large"
        self.random_inst.seed(seed)
        return (', '.join(self.random_inst.sample(self.SAVED_PROMPTS, k=count)),)
