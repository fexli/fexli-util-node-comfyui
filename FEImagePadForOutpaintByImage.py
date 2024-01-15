from .categories import CATE_IMAGE
import torch

MAX_RESOLUTION = 8192


class FEImagePadForOutpaintByImage:
    """
    基于双图像的外扩节点，便于图像生成
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inner_image": ("IMAGE",),
                "outer_image": ("IMAGE",),
                "padding_x": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "padding_xc": (["left", "right"],),
                "padding_y": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "padding_yc": (["top", "bottom"],),

                "feathering": ("INT", {"default": 50, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "expand_image"
    CATEGORY = CATE_IMAGE

    def expand_image(
            self, inner_image, outer_image, padding_x, padding_xc, padding_y, padding_yc, feathering
    ):
        batch_size, img_h, img_w, colors = inner_image.size()
        batch_size_o, img_h_o, img_w_o, colors_o = outer_image.size()
        if batch_size_o != batch_size:
            outer_image = outer_image[0, :, :, :].repeat(batch_size, 1, 1, 1)
        if colors_o != colors:
            raise ValueError("inner_image and outer_image must have the same number of channels")
        pl = padding_x
        if padding_xc == "right":
            pl = img_w_o - img_w - padding_x
        pt = padding_y
        if padding_yc == "bottom":
            pt = img_h_o - img_h - padding_y

        new_image = outer_image.clone()
        new_image[:, pt:pt + img_h, pl:pl + img_w, :] = inner_image

        mask = torch.ones((img_h_o, img_w_o), dtype=torch.float32)

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

            mask[pt:pt + img_h, pl:pl + img_w] = t
        else:
            mask[pt:pt + img_h, pl:pl + img_w] = torch.zeros(
                (img_h, img_w),
                dtype=torch.float32,
            )
        return (new_image, mask,)
