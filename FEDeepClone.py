from .utils.any_hack import any
from .categories import CATE_UTILS
from copy import deepcopy


class FEDeepClone:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (any,),
                "count": ("INT", {"default": 4, "min": 1, "max": 256, "step": 1}),
            },
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("output",)
    FUNCTION = "clone"
    CATEGORY = CATE_UTILS
    OUTPUT_IS_LIST = (True,)

    def clone(self, input, count):
        out = []
        for i in range(count):
            out.append(deepcopy(input))
        return (out,)
