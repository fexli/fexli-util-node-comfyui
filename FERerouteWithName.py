from .categories import CATE_UTILS
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode


class FERerouteWithName(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (any,),
                "note": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ('output',)
    FUNCTION = "output"
    CATEGORY = CATE_UTILS
    OUTPUT_NODE = True

    def output(self, input, note):
        return (input,)
