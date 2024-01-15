from .categories import CATE_UTILS
from .utils.color import pad_color
import random


class FERandomizedColorOut:
    """
    生成随机RGB颜色，用于OutPaint生成扩展绘板使用
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "red_prefer": (["random", "r+", "r~", "r-"], {"default": "random"}),
                "green_prefer": (["random", "g+", "g~", "g-"], {"default": "random"}),
                "blue_prefer": (["random", "b+", "b~", "b-"], {"default": "random"}),
            }
        }

    RETURN_TYPES = ("RGB_COLOR",)
    RETURN_NAMES = ('color',)
    FUNCTION = "send_color"
    CATEGORY = CATE_UTILS

    def randcolor(self, prefer):
        range_ = (-10, 265)
        if "+" in prefer:
            range_ = (128, 265)
        elif "-" in prefer:
            range_ = (-10, 128)
        elif "~" in prefer:
            range_ = (64, 191)
        return range_

    def send_color(self, seed, red_prefer, green_prefer, blue_prefer):
        c = pad_color(
            self.randcolor(red_prefer),
            self.randcolor(green_prefer),
            self.randcolor(blue_prefer),
            seed
        )
        return (c,)
