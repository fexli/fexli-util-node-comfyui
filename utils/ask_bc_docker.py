import time

import requests
import json
from typing import List

from requests.adapters import HTTPAdapter
from urllib3 import Retry
from ..config.configs import config
import sseclient


class PromptItem:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def __str__(self):
        return f"Promt[{self.role}:{self.content}]"

def bc_docker_ask_stream(
        messages: List[PromptItem],
        temperature=0.01,
        repetition_penalty=1.05,
        max_new_tokens=2048,
        top_p=0.85,
        top_k=5,
):
    inputs = ""
    for _ in messages:
        inputs += "<C_Q>" if _.role == "user" else "<C_A>"
        inputs += _.content
    if len(messages) > 0 and messages[-1].role == "user":
        inputs += "<C_A>"
    params_bc_tgi = {
        "inputs": inputs,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "repetition_penalty": repetition_penalty,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "do_sample": True,
            "details": False,
            "stream": True,
        }
    }
    result = None
    retry_strategy = Retry(
        total=1,  # 最大重试次数（包括首次请求）
        backoff_factor=1,  # 重试之间的等待时间因子
        status_forcelist=[429, 500, 502, 503, 504, 404],  # 需要重试的状态码列表
        allowed_methods=["POST"]  # 只对POST请求进行重试
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    # 创建会话并添加重试逻辑
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    for i in range(10):
        try:
            response = session.post(
                config.get("bc_docker_api"), headers={"User-Agent": "bc-ccui-agents/0.0.0"},
                json=params_bc_tgi, stream=True, timeout=30
            )
            if response.status_code != 200:
                print(f"bc_docker_ask_stream: {response.status_code} {response.text}")
                continue
            sse = sseclient.SSEClient(response)
            for msg in sse.events():
                if msg.data != '[DONE]':
                    dd = json.loads(msg.data)['token'].get('text', '')
                    if dd.endswith("</s>"):
                        break
                    yield dd
            break
        except Exception as e:
            import traceback
            traceback.print_exc()
            time.sleep(2)
            continue
