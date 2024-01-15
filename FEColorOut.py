from .categories import CATE_UTILS
from .utils.color import pad_color


class FEColorOut:
    """
    生成RGB颜色
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "red": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "green": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "blue": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            }
        }

    RETURN_TYPES = ("RGB_COLOR",)
    RETURN_NAMES = ('color',)
    FUNCTION = "send_color"
    CATEGORY = CATE_UTILS

    def send_color(self, red, green, blue):
        return (pad_color(red, green, blue, -1),)
