from .categories import CATE_GEN
from .utils.ask_bc_docker import bc_docker_ask_stream, PromptItem
from .utils.node_defs import FEAlwaysChangeNode
from .utils.any_hack import any


class FEGenStringBCDocker(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"default": "Hello World!", "multiline": True, "dynamicPrompts": False}),
                "temperature": ("FLOAT", {"default": 0.5, "min": 0, "max": 2, "step": 0.01}),
                "repetition_penalty": ("FLOAT", {"default": 1.05, "min": 0, "max": 10, "step": 0.01}),
                "max_new_tokens": ("INT", {"default": 2048, "min": 0, "max": 2048, "step": 1}),
                "top_p": ("FLOAT", {"default": 0.85, "min": 0.01, "max": 2, "step": 0.01}),
                "top_k": ("INT", {"default": 5, "min": 0, "max": 100, "step": 1}),
                "async_infer": (["YES", "NO"], {"default": "NO"}),
            },
            "optional": {
                "prompt_list": ("PROMPTS",),
            },
        }

    RETURN_TYPES = ("STRING", "BCD_GEN_CTX")
    RETURN_NAMES = ('prompt', 'generate_ctx')
    FUNCTION = "query"
    CATEGORY = CATE_GEN
    OUTPUT_NODE = True

    def query(
            self, user_prompt, temperature, repetition_penalty, max_new_tokens, top_p, top_k, async_infer,
            prompt_list=None
    ):
        if async_infer == "YES":
            args = {
                "user_prompt": user_prompt,
                "prompt_list": prompt_list,
                "temperature": temperature,
                "repetition_penalty": repetition_penalty,
                "max_new_tokens": max_new_tokens,
                "top_p": top_p,
                "top_k": top_k,
                # "seed": seed,
            }
            return ("", args,)
        result = ""
        print("generating prompt...", end="")
        if prompt_list is None:
            prompt_list = [PromptItem("user", user_prompt)]
        else:
            prompt_list = prompt_list['prompts']
        for _ in bc_docker_ask_stream(
                prompt_list, temperature=temperature, repetition_penalty=repetition_penalty,
                max_new_tokens=max_new_tokens, top_p=top_p, top_k=top_k):
            result += _
            # print(_, end="")
        print("...done")
        return (result, {},)
