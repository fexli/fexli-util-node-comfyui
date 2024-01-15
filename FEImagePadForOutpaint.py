from .utils.color import extract_pad_color, get_empty_color
from .categories import CATE_IMAGE
import torch

MAX_RESOLUTION = 8192


class FEImagePadForOutpaint:
    """
    图像外扩节点，便于图像生成
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "left": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8}),
                "top": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8}),
                "right": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8}),
                "bottom": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 8}),
                "feathering": ("INT", {"default": 50, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "pad_color": ("RGB_COLOR", {"default": get_empty_color()}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "expand_image"
    CATEGORY = CATE_IMAGE

    def expand_image(self, image, left, top, right, bottom, feathering, pad_color):
        batch_size, img_h, img_w, colors = image.size()

        colors = extract_pad_color(pad_color, batch_size) / 255
        new_image = torch.ones(
            (batch_size, img_h + top + bottom, img_w + left + right, 3),
            dtype=torch.float32,
        ).expand(batch_size, -1, -1, -1) * colors.view(batch_size, 1, 1, 3)

        new_image[:, top:top + img_h, left:left + img_w, :] = image

        mask = torch.ones(
            (img_h + top + bottom, img_w + left + right),
            dtype=torch.float32,
        )

        # 处理mask羽化
        if feathering > 0 and feathering * 2 < img_h and feathering * 2 < img_w:
            # distances to border
            mi, mj = torch.meshgrid(
                torch.arange(img_h, dtype=torch.float32),
                torch.arange(img_w, dtype=torch.float32),
                indexing='ij',
            )
            distances = torch.minimum(
                torch.minimum(mi, mj),
                torch.minimum(img_h - 1 - mi, img_w - 1 - mj),
            )
            # convert distances to square falloff from 1 to 0
            t = (feathering - distances) / feathering
            t.clamp_(min=0)
            t.square_()

            mask[top:top + img_h, left:left + img_w] = t
        else:
            mask[top:top + img_h, left:left + img_w] = torch.zeros(
                (img_h, img_w),
                dtype=torch.float32,
            )
        return (new_image, mask)
