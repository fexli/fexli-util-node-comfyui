import numpy as np
from .utils.color import extract_pad_color, get_empty_color, get_null_color
import torch
from .categories import CATE_TEST


class FEColor2Image:
    """
    生成RGB颜色
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "colorLU": ("RGB_COLOR", {"default": get_empty_color()}),
                "height": ("INT", {"default": 512, "min": 0, "max": 8192, "step": 8}),
                "width": ("INT", {"default": 512, "min": 0, "max": 8192, "step": 8}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1}),
                "batch_rand": (['true', 'false'],)
            },
            "optional": {
                "colorLD": ("RGB_COLOR", {"default": get_null_color()}),
                "colorRU": ("RGB_COLOR", {"default": get_null_color()}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('image',)
    FUNCTION = "build_image"
    CATEGORY = CATE_TEST

    def build_image(self, colorLU, height, width, batch_size, colorLD=None, colorRU=None, batch_rand="false"):
        if batch_rand == "true":
            t_batch_size = batch_size
            e_batch_size = -1
        else:
            t_batch_size = 1
            e_batch_size = batch_size
        color_lt = extract_pad_color(colorLU, t_batch_size)
        color_lt = color_lt.expand(e_batch_size, 3)
        if colorLD is None:
            colorLD = colorLU
        color_lb = extract_pad_color(colorLD, t_batch_size).expand(e_batch_size, 3)
        if colorRU is None:
            colorRU = colorLU
        color_rt = extract_pad_color(colorRU, t_batch_size).expand(e_batch_size, 3)

        image = torch.zeros((batch_size, height, width, 3), dtype=torch.float32)

        weight_rt = torch.linspace(0, 1, steps=width).view(1, -1, 1)
        weight_lb = torch.linspace(0, 1, steps=height).view(-1, 1, 1)
        weight_lt = 1 - weight_rt - weight_lb

        for _ in range(color_lt.shape[0]):
            image[_, :, :, :] = weight_lt * color_lt[_] + weight_rt * color_rt[_] + weight_lb * color_lb[_]

        image = image / 255.0
        return (image,)
