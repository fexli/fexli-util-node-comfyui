import random
import torch


def get_color(a, batch_size=1):
    if not isinstance(a, list) and not isinstance(a, tuple):
        return [a] * batch_size
    a1, a2 = a[:2]
    if a1 == a2:
        return [a1] * batch_size
    if a1 > a2:
        a1, a2 = a2, a1
    return [max(min(random.randint(a1, a2), 255), 0) for _ in range(batch_size)]


def extract_pad_color(pad_color, batch_size=1):
    r = pad_color.get("r", 0)
    g = pad_color.get("g", 0)
    b = pad_color.get("b", 0)
    s = pad_color.get("s", 0)

    random.seed(s)
    r = get_color(r, batch_size)
    g = get_color(g, batch_size)
    b = get_color(b, batch_size)
    rst = torch.stack([torch.tensor(r, dtype=torch.float32), torch.tensor(g, dtype=torch.float32),
                       torch.tensor(b, dtype=torch.float32)], dim=-1)

    return rst


def pad_color(r, g, b, s):
    return {
        'r': r,
        'g': g,
        'b': b,
        's': s
    }


def get_empty_color():
    return pad_color(0, 0, 0, 0)


def get_null_color():
    return pad_color(-1, -1, -1, -1)
