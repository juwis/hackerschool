// 2018-12-11
//
// Blockly blocks to support servos.
//
// Author: Sascha.MuellerzumHagen@baslerweb.com

var COLOR_SERVO = 30;
var MACHINE_SERVO_PINS = [
    ['channel 1', '0'],
    ['channel 2', '1'],
    ['channel 3', '2'],
    ['channel 4', '3'],
    ['channel 5', '4'],
    ['channel 6', '5'],
    ['channel 7', '6'],
    ['channel 8', '7'],
    ['channel 9', '8'],
    ['channel 10', '9'],
    ['channel 11', '10'],
    ['channel 12', '11'],
    ['channel 13', '12'],
    ['channel 14', '13']
];

Blockly.Blocks.machine_servo_channel = {
    init: function () {
        this.setColour(COLOR_SERVO);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_SERVO_PINS), 'ServoChannel');
        this.setOutput(true, 'MachineServoChannel');

        this.setTooltip('Get the right number for the given servo channel.');
    }
};
Blockly.Python.machine_servo_channel = function(block) {
    var channel = block.getFieldValue('ServoChannel');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};


Blockly.Blocks.servo_object = {
    init: function () {
        this.setColour(COLOR_SERVO);

        this.appendValueInput('VAR')
            .setCheck('MachineServoChannel')
            .appendField('create servo on');
        this.setOutput(true, 'Servo');

        this.setTooltip('Create a servo object which is conntected to the given channel.');
    }
};
Blockly.Python.servo_object = function (block) {
    Blockly.Python.definitions_.import_servo = 'from hucon import Servo';
    var argument0 = Blockly.Python.valueToCode(block, 'VAR', Blockly.Python.ORDER_ATOMIC) || 'NULL';

    var code = 'Servo(' + argument0 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.servo_set_offset = {
    init: function () {
        this.setColour(COLOR_SERVO);

        this.appendDummyInput()
            .appendField('set')
            .appendField(new Blockly.FieldVariable('servo'), 'VAR');
        this.appendValueInput('Offset')
            .setCheck('Number')
            .appendField('offset');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip('Set the servo offset. The Value can be between -100 and 100.');
    }
};
Blockly.Python.servo_set_offset = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var offset = Blockly.Python.valueToCode(block, 'Offset', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = varName + '.offset = ' + offset + '\n';
    return code;
};

Blockly.Blocks.servo_set_angle = {
    init: function () {
        this.setColour(COLOR_SERVO);

        this.appendDummyInput()
            .appendField('set')
            .appendField(new Blockly.FieldVariable('servo'), 'VAR');
        this.appendValueInput('Angle')
            .setCheck('Number')
            .appendField('angle');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip('Set the servo angle between 0 and 180 degree.');
    }
};
Blockly.Python.servo_set_angle = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var angle = Blockly.Python.valueToCode(block, 'Angle', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = varName + '.set_angle(' + angle + ')\n';
    return code;
};
