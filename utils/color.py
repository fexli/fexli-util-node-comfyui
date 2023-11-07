def extract_pad_color(pad_color):
    r = pad_color.get("red", 0)
    g = pad_color.get("green", 0)
    b = pad_color.get("blue", 0)
    return r, g, b
