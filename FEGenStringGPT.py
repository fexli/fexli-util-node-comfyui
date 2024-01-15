from .categories import CATE_GEN
from .utils.ask_stream import openai_ask_stream
from .config.configs import config
from .utils.node_defs import FEAlwaysChangeNode


class FEGenStringGPT(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "system_prompt": (
                    "STRING",
                    {"default": "You are ChatGPT, a large language model trained by OpenAI.", "multiline": True, "dynamicPrompts": False}
                ),

                "user_prompt": ("STRING", {"default": "Hello World!", "multiline": True}),
                "model": ("STRING", {"default": "gpt-4", "multiline": False}),
                "api": (config["openai_host"],),
                "temperature": ("FLOAT", {"default": 1, "min": 0, "max": 2, "step": 0.01}),
                "presence_penalty": ("FLOAT", {"default": 0, "min": 0, "max": 10, "step": 0.01}),
                "max_tokens": ("INT", {"default": 2048, "min": 0, "max": 2048, "step": 1}),
                "async_infer": (["YES", "NO"], {"default": "NO"}),
            }
        }

    RETURN_TYPES = ("STRING", "GPT_GEN_CTX")
    RETURN_NAMES = ('prompt', 'generate_ctx')
    FUNCTION = "query"
    CATEGORY = CATE_GEN
    OUTPUT_NODE = True

    def query(self, system_prompt, user_prompt, api, model, temperature, presence_penalty, max_tokens, async_infer):
        if async_infer == "YES":
            args = {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "model": model,
                "temperature": temperature,
                "presence_penalty": presence_penalty,
                "max_tokens": max_tokens,
                # "seed": seed,
            }
            return ("", args,)
        result = ""
        print("generating prompt...", end="")
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        if user_prompt:
            msgs.append({"role": "user", "content": user_prompt})
        for _ in openai_ask_stream(
                msgs, temperature=temperature, model=model, presence_penalty=presence_penalty, max_tokens=max_tokens,
                api=api):
            result += _
            print(_, end="")
        print("...done")
        return (result, {},)
