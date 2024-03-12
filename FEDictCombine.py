from .categories import CATE_UTILS
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode


class FEDictCombine(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {"input": (any, {"default": None})},
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = (any,)
    RETURN_NAMES = ('output',)
    FUNCTION = "out"
    CATEGORY = CATE_UTILS

    def out(self, **kwargs):
        output = {}
        for v in kwargs.values():
            output.update(v)
        return (output,)
