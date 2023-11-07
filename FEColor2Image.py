from .utils.color import extract_pad_color
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
                "colorLU": ("RGB_COLOR", {"default": {"red": 0, "green": 0, "blue": 0}}),
                "height": ("INT", {"default": 512, "min": 0, "max": 8192, "step": 8}),
                "width": ("INT", {"default": 512, "min": 0, "max": 8192, "step": 8}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1}),
            },
            "optional": {
                "colorLD": ("RGB_COLOR", {"default": {"red": -1, "green": -1, "blue": -1}}),
                "colorRU": ("RGB_COLOR", {"default": {"red": -1, "green": -1, "blue": -1}}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('image',)
    FUNCTION = "build_image"
    CATEGORY = CATE_TEST

    def build_image(self, colorLU, height, width, batch_size, colorLD=None, colorRU=None):
        color_lt = torch.tensor([*extract_pad_color(colorLU)], dtype=torch.float32)
        if colorLD is None:
            colorLD = colorLU
        color_lb = torch.tensor([*extract_pad_color(colorLD)], dtype=torch.float32)
        if colorRU is None:
            colorRU = colorLU
        color_rt = torch.tensor([*extract_pad_color(colorRU)], dtype=torch.float32)

        image = torch.zeros(height, width, 3)

        for i in range(height):
            for j in range(width):
                weight_rt = j / width
                weight_lb = i / height
                weight_lt = 1 - weight_rt - weight_lb
                image[i, j] = weight_lt * color_lt + weight_rt * color_rt + weight_lb * color_lb

        image = (image.repeat(batch_size, 1, 1, 1) / 255)

        return (image,)
