from ..categories import CATE_OP
from ..utils.any_hack import any


class FEOperatorIf:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "true": (any,),
                "false": (any,),
                "cond": ("BOOLEAN",),

            },
            "optional": {},
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = (any,)
    RETURN_NAMES = ('output',)
    FUNCTION = "out"
    CATEGORY = CATE_OP

    def out(self, true, false, cond):
        return (true if cond else false,)
