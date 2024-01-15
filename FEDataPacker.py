from .utils.any_hack import any
from .categories import CATE_UTILS


class FEDataPacker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {"input": (any,)},
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("output",)
    FUNCTION = "pack"
    CATEGORY = CATE_UTILS
    OUTPUT_IS_LIST = (True,)

    def pack(self, **kwargs):
        ret = (list(kwargs.values()),)
        return ret
