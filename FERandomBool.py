import os

from .categories import CATE_UTILS
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode
from random import Random


class FERandomBool(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "true_prob": ("FLOAT", {"default": 0.5, "min": 0, "max": 1, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ('bool',)
    FUNCTION = "get_rand"
    random_inst = Random()

    OUTPUT_NODE = True

    CATEGORY = CATE_UTILS

    def get_rand(self, true_prob, seed):
        self.random_inst.seed(seed)
        return (self.random_inst.random() < true_prob,)
