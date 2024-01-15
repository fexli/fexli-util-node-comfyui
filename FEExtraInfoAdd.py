from .categories import CATE_UTILS
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode
class FEExtraInfoAdd(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "save_field": ("STRING", {"default": "positive_prompt", "multiline": False}),
                "enter": (any,),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = ()
    FUNCTION = "write_extra"

    OUTPUT_NODE = True

    CATEGORY = CATE_UTILS

    def write_extra(self, save_field, enter=None, unique_id=None, extra_pnginfo=None):
        if extra_pnginfo is not None:
            extra_pnginfo[save_field] = enter
        else:
            print("WARN: extra_pnginfo is missing")
        return {}
