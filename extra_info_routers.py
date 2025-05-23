import json
import os.path

import comfy.samplers  # noqa
import folder_paths  # noqa
from aiohttp import web


def get_req_param(request, param, default=None):
    return request.rel_url.query[param] if param in request.rel_url.query else default


def get_folder_path(file: str, model_type="loras"):
    file_path = folder_paths.get_full_path(model_type, file) or ""
    if file_path and not os.path.exists(file_path):
        file_path = os.path.abspath(file_path) or ""
    if not os.path.exists(file_path):
        file_path = None
    return file_path or None


def get_dict_value(data: dict, dict_key: str, default=None):
    keys = dict_key.split('.')
    key = keys.pop(0) if len(keys) > 0 else None
    found = data[key] if key in data else None
    if found is not None and len(keys) > 0:
        return get_dict_value(found, '.'.join(keys), default)
    return found if found is not None else default


def _merge_metadata(info_data: dict, data_meta: dict):
    base_model_file = get_dict_value(data_meta, 'ss_sd_model_name', None)
    if base_model_file:
        info_data['baseModelFile'] = base_model_file

    # Loop over metadata tags
    trained_words = {}
    if 'ss_tag_frequency' in data_meta and isinstance(data_meta['ss_tag_frequency'], dict):
        for bucket_value in data_meta['ss_tag_frequency'].values():
            if isinstance(bucket_value, dict):
                for tag, count in bucket_value.items():
                    if tag not in trained_words:
                        trained_words[tag] = {'word': tag, 'count': 0, 'metadata': True}
                    trained_words[tag]['count'] = trained_words[tag]['count'] + count

    if 'trainedWords' not in info_data:
        info_data['trainedWords'] = list(trained_words.values())
    else:
        merged_dict = {}
        for existing_word_data in info_data['trainedWords']:
            merged_dict[existing_word_data['word']] = existing_word_data
        for new_key, new_word_data in trained_words.items():
            if new_key not in merged_dict:
                merged_dict[new_key] = {}
            merged_dict[new_key] = {**merged_dict[new_key], **new_word_data}
        info_data['trainedWords'] = list(merged_dict.values())

    info_data['raw']['metadata'] = data_meta

    if 'sha256' not in info_data and '_sha256' in data_meta:
        info_data['sha256'] = data_meta['_sha256']


def _get_model_metadata(file: str, model_type="loras", default=None):
    file_path = get_folder_path(file, model_type)
    data = None
    try:
        if not file_path.endswith('.safetensors'):
            return None
        with open(file_path, "rb") as file:
            # https://github.com/huggingface/safetensors#format
            # 8 bytes: N, an unsigned little-endian 64-bit integer, containing the size of the header
            header_size = int.from_bytes(file.read(8), "little", signed=False)

            if header_size <= 0:
                raise BufferError("Invalid header size")

            header = file.read(header_size)
            if header is None:
                raise BufferError("Invalid header")

            header_json = json.loads(header)
            data = header_json["__metadata__"] if "__metadata__" in header_json else None

            if data is not None:
                for key, value in data.items():
                    if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
                        try:
                            value_as_json = json.loads(value)
                            data[key] = value_as_json
                        except Exception:
                            print(f'metdata for field {key} did not parse as json')
    except:
        data = None
    return data if data is not None else default


async def get_model_info(
        file: str,
        model_type="loras",
        default=None
):
    file_path = get_folder_path(file, model_type)
    if file_path is None:
        return default
    info_data = {}
    try_info_path = f'{file_path}.weilin-info.json'
    if os.path.exists(try_info_path):  # load weilin-type lora-info
        try:
            with open(try_info_path) as f:
                info_data = json.load(f)
        except:
            pass
    if 'file' not in info_data:
        info_data['file'] = file
    if 'path' not in info_data:
        info_data['path'] = file_path

    if 'raw' not in info_data:
        info_data['raw'] = {}
    data_meta = _get_model_metadata(
        file,
        model_type=model_type,
        default={},
    )
    _merge_metadata(info_data, data_meta)
    if 'trainedWords' in info_data:
        # Sort by count; if it doesn't exist, then assume it's a top item from civitai or elsewhere.
        info_data['trainedWords'] = sorted(
            info_data['trainedWords'],
            key=lambda w: w['count'] if 'count' in w else 99999,
            reverse=True
        )
    return info_data


async def get_loras_info_response(request):
    api_response = {'status': 200, "data": {}}
    lora_file = get_req_param(request, 'file')
    if lora_file is not None:
        print(f'get_loras_info_response: {lora_file}')
        info_data = await get_model_info(lora_file)
        if info_data is None:
            api_response['status'] = '404'
            api_response['error'] = 'No Lora found at path'
        else:
            api_response['data'] = info_data
    else:
        api_response['status'] = '400'
        api_response['error'] = 'Lora name is empty'
    return api_response


def register(path, routes):
    @routes.get(f'/fe-util/{path}/samplers')
    async def get_samplers(request):
        return web.json_response(comfy.samplers.KSampler.SAMPLERS)

    @routes.get(f'/fe-util/{path}/schedulers')
    async def get_schedulers(request):
        return web.json_response(comfy.samplers.KSampler.SCHEDULERS)

    @routes.get(f"/fe-util/{path}/loras/info")
    async def get_loras_info(request):
        api_response = await get_loras_info_response(request)
        return web.json_response(api_response)
