import typing
import uuid

from urllib3 import Retry
import sseclient
from requests.adapters import HTTPAdapter
import requests
import time
import json
from ..config.configs import config

openai_header = {'Content-Type': 'application/json',
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
                               "like Gecko) Chrome/114.0.0.0 Safari/537.36"}
if openai_key := config.get("openai_key"):
    openai_header["Authorization"] = f"Bearer {openai_key}"


def openai_ask_stream(
        messages: typing.List, api: str, model='gpt-4', history=None,
        temperature: float = 0.01, presence_penalty=1, max_tokens=2048, retry=100,
        custom_header: typing.Union[dict, None] = None,
):
    if history is None:
        history = []
    if not isinstance(history, list):
        history = []
    params_gpt = {
        "model": model,
        "messages": history + messages,
        'temperature': temperature,
        "presence_penalty": presence_penalty,
        "max_tokens": max_tokens,
        "stream": True,
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
    for i in range(retry):
        try:
            headersq = openai_header.copy()
            if custom_header:
                headersq.update(custom_header)
            response = session.post(
                api, headers=headersq,
                data=json.dumps(params_gpt),
                stream=True
            )
            sse = sseclient.SSEClient(response)
            for msg in sse.events():
                if msg.data != '[DONE]':
                    dd = json.loads(msg.data)['choices'][0]['delta'].get('content', '')
                    yield dd
            break
        except Exception as e:
            import traceback
            traceback.print_exc()
            time.sleep(2)
            continue


def openai_ask_background(
        model_name: str,
        background: typing.Dict,
        pkw_list: typing.List,
        api: str,
):
    """
    使用session对openai进行问答，返回content(翻译成中文)
    :return: yield content
    """
    params_gpt = {
        "model": model_name,
        "conversation_id": uuid.uuid4().hex[:6],
        "background": background,
        "pkw_list": pkw_list,
        'temperature': 0,
        "presence_penalty": 0,
        "stream": True,
    }
    result = None
    retry_strategy = Retry(
        total=1,  # 最大重试次数（包括首次请求）
        backoff_factor=1,  # 重试之间的等待时间因子
        status_forcelist=[400, 404, 429, 500, 502, 503, 504],  # 需要重试的状态码列表
        allowed_methods=["POST"]  # 只对POST请求进行重试
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    # 创建会话并添加重试逻辑
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    for i in range(20):
        try:
            response = session.post(
                api, headers=openai_header.copy(),
                data=json.dumps(params_gpt), stream=True
            )
            sse = sseclient.SSEClient(response)
            rst = ""
            for msg in sse.events():
                if msg.data != '[DONE]':
                    dd = json.loads(msg.data)['choices'][0]['delta'].get('content', '')
                    # print(f"\033[33m{dd}\033[0m",end='', flush=True)

                    if "pkw" in dd and "<background>" in dd and "<pkwlist>" in dd:
                        pkwlist = json.loads(dd.split("<pkwlist>")[1])[:-1]
                        background = json.loads(dd.split("<background>")[1].split("<pkwlist>")[0])
                        pkw = json.loads(dd.split("<pkw>")[1].split("<background>")[0])
                        return rst, pkw, pkwlist, background
                    else:
                        rst += dd

            if rst == "":
                raise Exception("openai ask stream is empty")

        except Exception as e:
            import traceback
            traceback.print_exc()
            time.sleep(2)
            continue
    return None, None, None, None
