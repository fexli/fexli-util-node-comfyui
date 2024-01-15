from .utils.any_hack import any
from .categories import CATE_UTILS


class FEDictUnpacker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_dict": (any,),
                "out_field": ("STRING", {"default": "a,b"},),
            },
        }

    @classmethod
    def VALIDATE_OUTPUTS(s, **kwargs):
        return True

    RETURN_TYPES = tuple(any for _ in range(32))
    RETURN_NAMES = tuple("field" for _ in range(32))
    FUNCTION = "unpack"
    CATEGORY = CATE_UTILS

    def unpack(self, input_dict, out_field):
        print("input_dict",input_dict)
        return tuple([input_dict.get(_) for _ in out_field.split(",")])
