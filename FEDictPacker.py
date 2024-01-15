from .utils.any_hack import any
from .categories import CATE_UTILS


class FEDictPacker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "in_field": ("STRING", {"default": "a,b", "forceInput": False},),
            },
            "optional": {"input": (any,)},
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("output",)
    FUNCTION = "pack"
    CATEGORY = CATE_UTILS

    def pack(self, in_field, **kwargs):
        print("FEDictPacker.pack",kwargs)
        ret = {}
        for i, e in enumerate([_ for _ in in_field.split(",")]):
            ret[e] = list(kwargs.values())[int(i)]
        return (ret,)
