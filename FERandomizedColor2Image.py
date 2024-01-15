import torch
from .categories import CATE_TEST


class FERandomizedColor2Image:
    """
    生成随机RGB颜色
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "height": ("INT", {"default": 512, "min": 0, "max": 8192, "step": 8}),
                "width": ("INT", {"default": 512, "min": 0, "max": 8192, "step": 8}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('image',)
    FUNCTION = "build_image"
    CATEGORY = CATE_TEST

    def build_image(self, seed, height, width, batch_size):
        image = torch.randn((batch_size, height, width, 3), generator=torch.manual_seed(seed), dtype=torch.float32)

        return (image,)
