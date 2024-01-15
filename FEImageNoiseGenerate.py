import torch
from .categories import CATE_TEST


class FEImageNoiseGenerate:
    """
    生成随机RGB颜色
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "shake": ("FLOAT", {"default": 0.1, "min": 0, "max": 1, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ('image',)
    FUNCTION = "build_image"
    CATEGORY = CATE_TEST

    def build_image(self, image, seed, shake):
        batch_size, img_h, img_w, colors = image.size()
        # random shake for each pixel
        shake_im = (torch.rand((batch_size, img_h, img_w, colors), generator=torch.manual_seed(seed),
                               dtype=torch.float32) - 0.5) * shake * 2
        new_image = image + shake_im
        new_image.clamp_(min=0, max=1)

        return (new_image,)
