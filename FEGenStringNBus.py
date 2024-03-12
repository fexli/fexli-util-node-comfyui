from .categories import CATE_GEN
from .utils.ask_stream import openai_ask_background
from .config.configs import config
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode


class FEGenStringNBus(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pkws": (any,),
                "api": ("STRING", {"default": config["nbus_api"], "multiline": False}),
                "model": ("STRING", {"default": "sd_axl3plus_v2", "multiline": False}),
            },
            "optional": {
                "background": (any,),
            }
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING", any)
    RETURN_NAMES = ('prompt', 'pkw')
    FUNCTION = "query"
    CATEGORY = CATE_GEN
    OUTPUT_NODE = True

    def query(self, pkws, api, model, background=None):
        if background is None or not background:
            background = {}
        if isinstance(background, list):
            background = background[0]
        if not api:
            api = config["nbus_api"]
        if isinstance(api, list):
            api = api[0]
        if isinstance(model, list):
            model = model[0]

        print("generating prompt...", end="")
        result, pkw, _, _ = openai_ask_background(
            model_name=model, background=background, pkw_list=pkws, api=api)
        print("done")
        return (result, pkw,)
