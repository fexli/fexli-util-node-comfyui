from .categories import CATE_UTILS
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode


class FEAnyToDict(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (any,),
                "field": ("STRING", {"default": "field_name", "multiline": False}),
            },
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ('output',)
    FUNCTION = "output"
    CATEGORY = CATE_UTILS
    OUTPUT_NODE = True

    def output(self, input, field):
        return ({field: input},)
