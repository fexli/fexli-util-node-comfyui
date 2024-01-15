from .utils.any_hack import any
from .categories import CATE_UTILS


class FEDataInsertor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (any,),
                "append": (any,)
            },
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("output",)
    FUNCTION = "insert"
    CATEGORY = CATE_UTILS
    INPUT_IS_LIST = (True, True,)
    OUTPUT_IS_LIST = (True,)

    def insert(self, input, append):
        out = []
        out.extend(input)
        out.extend(append)
        return (out,)
