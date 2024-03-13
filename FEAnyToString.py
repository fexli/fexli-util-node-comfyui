import json

from .categories import CATE_UTILS
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode
from typing import Dict, List


class FEAnyToString(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (any,),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('output',)
    FUNCTION = "output"
    CATEGORY = CATE_UTILS
    OUTPUT_NODE = True

    def output(self, input):
        if isinstance(input, (Dict, List,)):
            return (json.dumps(input, ensure_ascii=False),)
        return (str(input),)
