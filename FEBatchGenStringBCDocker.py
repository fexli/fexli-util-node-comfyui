import comfy.utils  # noqa
from .categories import CATE_GEN
from .utils.ask_bc_docker import bc_docker_ask_stream, PromptItem
from .utils.job import Job


class FEBatchGenStringBCDocker:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompts": ("BCD_GEN_CTX",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ('prompt',)
    FUNCTION = "query"
    INPUT_IS_LIST = (True,)
    OUTPUT_IS_LIST = (True,)
    CATEGORY = CATE_GEN
    OUTPUT_NODE = True

    def get_result(self, kwds):
        result = ""
        if kwds.get("prompt_list", None) is not None:
            kwds["messages"] = kwds['prompt_list']['prompts']
        else:
            kwds["messages"] = [PromptItem("user", kwds['user_prompt'])]
        if "prompt_list" in kwds:
            del kwds['prompt_list']
        if "user_prompt" in kwds:
            del kwds['user_prompt']
        for _ in bc_docker_ask_stream(**kwds):
            result += _
        return result

    def query(self, user_prompts):
        steps = len(user_prompts)
        tasks = []
        for user_prompt in user_prompts:
            tasks.append(Job(target=self.get_result, args=(user_prompt,)))
        for task in tasks:
            task.start()
        result = []
        pbar = comfy.utils.ProgressBar(steps)
        for idx, task in enumerate(tasks):
            result.append(task.get_result(nJoin=True))
            pbar.update(1)
        return (result,)
