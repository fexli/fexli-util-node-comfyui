import {app} from "../../../scripts/app.js";
import {ComfyWidgets} from "../../../scripts/widgets.js";

const FE_DATA_PACKER = ["FEDataPacker", "FEDictPacker", "FETextCombine", "FEDictCombine", "FETextCombine2Any"];
const FE_DATA_UNPACKER = ["FEDataUnpacker", "FEDictUnpacker"];
const FORBIDDEN_INPUT_FIELDS = ["in_field"];
const LAST_TYPE = Symbol("LastType");

app.registerExtension({
    name: "fexli.DataPacker",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        const removeInput = nodeType.prototype.removeInput;
        if (FE_DATA_PACKER.includes(nodeData.name)) {
            nodeType.prototype.removeInput = function (slot) {
                this.disconnectInput(slot);
                var slot_info = this.inputs.splice(slot, 1);
                for (var i = slot; i < this.inputs.length; ++i) {
                    if (!this.graph) { // force close
                        break
                    }
                    if (!this.inputs[i]) {
                        continue;
                    }
                    var link = this.graph.links[this.inputs[i].link];
                    if (!link) {
                        continue;
                    }
                    link.target_slot -= 1;
                }
                this.setSize(this.computeSize());
                if (this.onInputRemoved) {
                    this.onInputRemoved(slot, slot_info[0]);
                }
                this.setDirtyCanvas(true, true);
            }
        }

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
            if (FE_DATA_UNPACKER.includes(nodeData.name)) {
                this.inputs[0].shape = 6
                for (let i = 0; i < this.outputs.length - 1; i++) {
                    if (!this.outputs[i].links || this.outputs[i].links.length === 0) {
                        this.removeOutput(i--);
                    }
                }
            }
        }


        if (FE_DATA_UNPACKER.includes(nodeData.name)) {
            nodeType.prototype.onConnectionsChange = function (type, _, connected, link_info) {
                // console.log("onConnectionsChange", this)
                for (let i = 0; i < this.outputs.length - 1; i++) {
                    if (!this.outputs[i].links || this.outputs[i].links.length === 0) {
                        console.log("onConnectionsChange pop", i, this.removeOutput(i--));
                    }
                }
                if (this.outputs[this.outputs.length - 1]?.links) {
                    this.addOutput("v" + +new Date(), this.outputs[0].type).label = "output";
                }
            };
        } else if (FE_DATA_PACKER.includes(nodeData.name)) {
            nodeType.prototype.onConnectionsChange = function (type, _, connected, link_info) {
                for (let i = 0; i < this.inputs.length - 1; i++) {
                    if (!this.inputs[i].link && !FORBIDDEN_INPUT_FIELDS.includes(this.inputs[i].name)) {
                        this.removeInput(i--);
                    }
                }
                if (!this.inputs.length) {
                    return
                }
                if (this.inputs[this.inputs.length - 1].link) {
                    this.addInput("v" + +new Date(), this.inputs[0].type).label = "input";
                }
            };
        }
    },
});
