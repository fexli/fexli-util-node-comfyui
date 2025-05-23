from .FEImagePadForOutpaint import FEImagePadForOutpaint
from .FEColorOut import FEColorOut
from .FEColor2Image import FEColor2Image
from .FERandomizedColor2Image import FERandomizedColor2Image
from .FERandomizedColorOut import FERandomizedColorOut
from .FESaveEncryptImage import FESaveEncryptImage
from .FEImagePadForOutpaintByImage import FEImagePadForOutpaintByImage
from .FEImageNoiseGenerate import FEImageNoiseGenerate
from .FEGenStringBCDocker import FEGenStringBCDocker
from .FETextInput import FETextInput
from .FETextCombine import FETextCombine
from .FEDataPacker import FEDataPacker
from .FEDataUnpacker import FEDataUnpacker
from .FEBatchGenStringBCDocker import FEBatchGenStringBCDocker
from .FEGenStringGPT import FEGenStringGPT
from .operate.FEOperatorIf import FEOperatorIf
from .FEExtraInfoAdd import FEExtraInfoAdd
from .FERandomPrompt import FERandomPrompt
from .FEDeepClone import FEDeepClone
from .FEDataInsertor import FEDataInsertor
from .FERandomLoraSelect import FERandomLoraSelect
from .FEDictUnpacker import FEDictUnpacker
from .FEDictPacker import FEDictPacker
from .FEEncLoraLoader import FEEncLoraLoader
from .FEBCPrompt import FEBCPrompt
from .FERerouteWithName import FERerouteWithName
from .FETextCombine2Any import FETextCombine2Any
from .FERandomBool import FERandomBool
from .FEInterruptCondition import FEInterruptCondition
from .FEDictCombine import FEDictCombine
from .FEAnyToDict import FEAnyToDict
from .FEGenStringNBus import FEGenStringNBus
from .FEAnyToString import FEAnyToString
from .FEEncLoraAutoLoader import FEEncLoraAutoLoader
from .FELoadImageQQUrl import FELoadImageQQUrl
from .FEEncLoraAutoLoaderStack import FEEncLoraAutoLoaderStack

from server import PromptServer  # noqa
from .extra_info_routers import register as ei_register

routes = PromptServer.instance.routes
ei_register("exinfo", routes)

NODE_CLASS_MAPPINGS = {
    "FEImagePadForOutpaint": FEImagePadForOutpaint,
    "FEColorOut": FEColorOut,
    "FEColor2Image": FEColor2Image,
    "FERandomizedColor2Image": FERandomizedColor2Image,
    "FERandomizedColorOut": FERandomizedColorOut,
    "FESaveEncryptImage": FESaveEncryptImage,
    "FEImagePadForOutpaintByImage": FEImagePadForOutpaintByImage,
    "FEImageNoiseGenerate": FEImageNoiseGenerate,
    "FEGenStringBCDocker": FEGenStringBCDocker,
    "FETextInput": FETextInput,
    "FETextCombine": FETextCombine,
    # "FEPythonStrOp": FEPythonStrOp,
    "FEDataPacker": FEDataPacker,
    "FEDataUnpacker": FEDataUnpacker,
    "FEBatchGenStringBCDocker": FEBatchGenStringBCDocker,
    "FEGenStringGPT": FEGenStringGPT,
    "FEOperatorIf": FEOperatorIf,
    "FEExtraInfoAdd": FEExtraInfoAdd,
    "FERandomPrompt": FERandomPrompt,
    "FEDeepClone": FEDeepClone,
    "FEDataInsertor": FEDataInsertor,
    "FERandomLoraSelect": FERandomLoraSelect,
    "FEDictUnpacker": FEDictUnpacker,
    "FEDictPacker": FEDictPacker,
    "FEEncLoraLoader": FEEncLoraLoader,
    "FEBCPrompt": FEBCPrompt,
    "FERerouteWithName": FERerouteWithName,
    "FETextCombine2Any": FETextCombine2Any,
    "FERandomBool": FERandomBool,
    "FEInterruptCondition": FEInterruptCondition,
    "FEDictCombine": FEDictCombine,
    "FEAnyToDict": FEAnyToDict,
    "FEGenStringNBus": FEGenStringNBus,
    "FEAnyToString": FEAnyToString,
    "FEEncLoraAutoLoader": FEEncLoraAutoLoader,
    "FELoadImageQQUrl": FELoadImageQQUrl,
    "FEEncLoraAutoLoaderStack": FEEncLoraAutoLoaderStack,
}

WEB_DIRECTORY = "./web"
