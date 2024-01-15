from .categories import CATE_UTILS


class FETextInput:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('output',)
    FUNCTION = "out"
    CATEGORY = CATE_UTILS

    def out(self, input):
        return (input,)
