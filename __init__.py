from .FEImagePadForOutpaint import FEImagePadForOutpaint
from .FEColorOut import FEColorOut
from .FEColor2Image import FEColor2Image
from .FERandomizedColor2Image import FERandomizedColor2Image

NODE_CLASS_MAPPINGS = {
    "FEImagePadForOutpaint": FEImagePadForOutpaint,
    "FEColorOut": FEColorOut,
    "FEColor2Image": FEColor2Image,
    "FERandomizedColor2Image": FERandomizedColor2Image,
}
