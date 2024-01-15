from .categories import CATE_UTILS
from .utils.any_hack import any
from .utils.node_defs import FEAlwaysChangeNode


class FEPythonStrOp(FEAlwaysChangeNode):

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pythonScript": ("STRING", {"default": """output = str_input.replace(" ","")""", "multiline": True, "dynamicPrompts": False}),
                "runner": (["exec", 'eval'], {"default": "exec"})
            },
            "optional": {
                "str_input": ("STRING", {"default": "", "multiline": True, "forceInput": True, "dynamicPrompts": False}),
                "int_input": ("INT", {"default": 0}),
                "float_input": ("FLOAT", {"default": 0.0}),
            }
        }

    RETURN_TYPES = (any,)
    RETURN_NAMES = ('output',)
    FUNCTION = "out"
    CATEGORY = CATE_UTILS

    def out(self, pythonScript, runner, str_input="", int_input=0, float_input=0.0):
        if runner == "eval":
            pythonScript = "output = " + pythonScript
        try:
            namespace = globals()
            namespace.update(locals())
            namespace.update({"str_input": str_input, "int_input": int_input, "float_input": float_input})
            exec(pythonScript, namespace)
            if "output" not in namespace:
                raise Exception(
                    "output not found (please assign to output variable, "
                    "existing variables: " + ", ".join(namespace.keys()) + ")"
                )
            output = namespace["output"]
        except Exception as e:
            output = str(e)
        return (output,)
