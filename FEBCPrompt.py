from .categories import CATE_GEN
from .utils.ask_bc_docker import PromptItem
from .utils.node_defs import FEAlwaysChangeNode


class FEBCPrompt(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "role": (["user", 'assistant'],),
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "prev_prompt": ("PROMPTS",),
            },
        }

    RETURN_TYPES = ("PROMPTS",)
    RETURN_NAMES = ('prompts',)
    FUNCTION = "output"
    CATEGORY = CATE_GEN
    OUTPUT_NODE = True

    def output(self, role, system_prompt, prev_prompt=None):
        if prev_prompt is None:
            prev_prompt = {"prompts": []}
        prev_prompt['prompts'].append(PromptItem(role, system_prompt))
        return (prev_prompt,)
