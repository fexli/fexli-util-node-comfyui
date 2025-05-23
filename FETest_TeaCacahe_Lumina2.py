import torch
import numpy as np
from comfy.ldm.common_dit import pad_to_patch_size
from .categories import CATE_UTILS

from unittest.mock import patch

# referenced from https://github.com/spawner1145/TeaCache/blob/main/TeaCache4Lumina2/teacache_lumina2.py
# transplanted by @fexli
def teacache_forward_working(
        self, x, timesteps, context, num_tokens, attention_mask=None, **kwargs
):
    # 初始化TeaCache相关参数
    cap_feats = context
    cap_mask = attention_mask
    bs, c, h, w = x.shape
    x = pad_to_patch_size(x, (self.patch_size, self.patch_size))
    t = (1.0 - timesteps).to(dtype=x.dtype)

    # 时间嵌入处理
    t_emb = self.t_embedder(t, dtype=x.dtype)
    adaln_input = t_emb

    # 文本特征嵌入
    cap_feats = self.cap_embedder(cap_feats)

    # 图像分块嵌入和位置编码
    x, mask, img_size, cap_size, freqs_cis = self.patchify_and_embed(x, cap_feats, cap_mask, t_emb, num_tokens)
    freqs_cis = freqs_cis.to(x.device)

    # TeaCache核心逻辑
    max_seq_len = x.shape[1]
    should_calc = True

    if hasattr(self, 'enable_teacache') and self.enable_teacache:
        # 初始化缓存
        cache_key = max_seq_len
        if cache_key not in self.cache:
            self.cache[cache_key] = {
                "accumulated_rel_l1_distance": 0.0,
                "previous_modulated_input": None,
                "previous_residual": None,
            }
        current_cache = self.cache[cache_key]

        # 计算调制输入
        modulated_inp = self.layers[0].adaLN_modulation(adaln_input.clone())[0]

        # 缓存更新逻辑
        if self.cnt == 0 or self.cnt == self.num_steps - 1:
            should_calc = True
            current_cache["accumulated_rel_l1_distance"] = 0.0
        else:
            if current_cache["previous_modulated_input"] is not None:
                # 多项式系数调整
                coefficients = [393.76566581, -603.50993606, 209.10239044, -23.00726601,
                                0.86377344]  # taken from teacache_lumina_next.py
                rescale_func = np.poly1d(coefficients)

                # 计算相对L1变化
                prev_mod_input = current_cache["previous_modulated_input"]
                prev_mean = prev_mod_input.abs().mean()
                if prev_mean.item() > 1e-9:
                    rel_l1_change = ((modulated_inp - prev_mod_input).abs().mean() / prev_mean).cpu().item()
                else:
                    rel_l1_change = 0.0 if modulated_inp.abs().mean().item() < 1e-9 else float('inf')

                # 累计变化量
                current_cache["accumulated_rel_l1_distance"] += rescale_func(rel_l1_change)

                # 阈值判断
                if current_cache["accumulated_rel_l1_distance"] < self.rel_l1_thresh:
                    should_calc = False
                else:
                    should_calc = True
                    current_cache["accumulated_rel_l1_distance"] = 0.0

        current_cache["previous_modulated_input"] = modulated_inp.clone()

        # 序列长度管理
        if not hasattr(self, 'uncond_seq_len'):
            self.uncond_seq_len = cache_key
        if cache_key != self.uncond_seq_len:
            self.cnt += 1
            if self.cnt >= self.num_steps:
                self.cnt = 0

    # 主处理流程
    if hasattr(self, 'enable_teacache') and self.enable_teacache and not should_calc:
        processed_x = x + current_cache["previous_residual"]
    else:
        original_x = x.clone()
        current_x = x
        for layer in self.layers:
            current_x = layer(current_x, mask, freqs_cis, adaln_input)

        if hasattr(self, 'enable_teacache') and self.enable_teacache:
            current_cache["previous_residual"] = current_x - original_x
        processed_x = current_x

    # 最终输出处理
    output = self.final_layer(processed_x, adaln_input)
    output = self.unpatchify(output, img_size, cap_size, return_tensor=True)[:, :, :h, :w]

    return -output


class FETest_TeaCacahe_Lumina2:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "rel_l1_thresh": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 10.0, "step": 0.001}),
                "steps": ("INT", {"default": 10, "min": 1, "max": 100, "step": 1}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch_teacache"
    CATEGORY = CATE_UTILS

    def patch_teacache(self, model, rel_l1_thresh, steps):
        if rel_l1_thresh == 0:
            return (model,)

        # 克隆模型并获取transformer
        model_clone = model.clone()
        transformer = model_clone.model.diffusion_model

        # 注入TeaCache属性
        transformer.__class__.enable_teacache = True
        transformer.__class__.cnt = 0
        transformer.__class__.num_steps = steps
        transformer.__class__.rel_l1_thresh = rel_l1_thresh
        transformer.__class__.cache = {}
        transformer.__class__.uncond_seq_len = None

        # 替换forward方法
        transformer.forward = teacache_forward_working.__get__(transformer, transformer.__class__)

        return (model_clone,)
