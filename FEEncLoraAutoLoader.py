from .utils.any_hack import any
from .FEEncLoraAutoLoaderStack import FEEncLoraAutoLoaderStack


class FEEncLoraAutoLoader(FEEncLoraAutoLoaderStack):
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "model_type": (["sd1.5", "sdxl", "sd3", "sd3.5", 'pony', 'il', 'noob', 'flux'],),
                "prompt": ("STRING", {"default": "", 'forceInput': True}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", 'STRING', any)
    RETURN_NAMES = ("MODEL", "CLIP", "prompt", "EXTRA")
    FUNCTION = "load_lora"

    CATEGORY = "loaders"

    def load_lora(self, model, clip, model_type, prompt, strength_model, strength_clip):
        stack, prompt, extra = self.load_lora_stack(model_type, prompt, strength_model, strength_clip)

        m = model
        c = clip
        # result = []
        lcnt = 0

        for name, model_s, clip_s in stack:
            lora_name = name
            # try:
            #     result = get_metadata(lora_name) or {}
            # except:
            #     result = {}
            if not lora_name:
                print("Failed to load lora with empty name", name)
                continue
            try:
                m, c = super().load_lora(m, c, lora_name, model_s, clip_s)
                lcnt += 1
            except:
                print("Failed to load lora with error occur", name)
                raise
        print("Auto Load", lcnt, "LLor ClipData")
        return (m, c, prompt, extra,)
