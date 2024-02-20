from .categories import CATE_UTILS
from .utils.any_hack import any


class FETextCombine2Any:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {"input": (any, {"default": None})},
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('output',)
    FUNCTION = "out"
    CATEGORY = CATE_UTILS

    def out(self, **kwargs):
        output = "".join([str(_) for _ in list(kwargs.values()) if _ is not None])
        return (output,)
