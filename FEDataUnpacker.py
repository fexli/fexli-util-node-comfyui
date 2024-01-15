from .utils.any_hack import any
from .categories import CATE_UTILS


class FEDataUnpacker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {"input": (any,)},
        }

    @classmethod
    def VALIDATE_OUTPUTS(s, **kwargs):
        return True

    RETURN_TYPES = tuple(any for _ in range(32))
    RETURN_NAMES = tuple("output" for _ in range(32))
    FUNCTION = "unpack"
    CATEGORY = CATE_UTILS
    INPUT_IS_LIST = (True,)

    def unpack(self, **kwargs):
        ret = tuple([_ for _ in kwargs['input']])
        return ret
