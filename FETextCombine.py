from .categories import CATE_UTILS


class FETextCombine:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {"input": ("STRING", {"default": "", 'forceInput': True})},
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('output',)
    FUNCTION = "out"
    CATEGORY = CATE_UTILS

    def out(self, **kwargs):
        if kwargs.get('input') == 'undefined':
            kwargs['input'] = ''
        if "input" in kwargs and not kwargs["input"]:
            del kwargs['input']
        output = "".join([str(_) for _ in list(kwargs.values())])
        return (output,)
