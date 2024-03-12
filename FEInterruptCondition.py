import requests
from comfy.cli_args import args  # noqa
from .utils.any_hack import any
from .categories import CATE_UTILS
from .utils.node_defs import FEAlwaysChangeNode


class FEInterruptCondition(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (any,),
            },
            "optional": {
                "interrupt": ("BOOLEAN", {"default": False, "forceInput": True}),
            },
        }

    FUNCTION = "interrupt"

    CATEGORY = CATE_UTILS
    RETURN_NAMES = ('output',)
    RETURN_TYPES = (any,)
    OUTPUT_NODE = True

    def interrupt(self, input, interrupt=False):
        if interrupt:
            requests.post(f"http://localhost:{args.port}/interrupt")
        return (input,)
