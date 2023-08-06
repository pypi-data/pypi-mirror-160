/*
    niryo_one_python_generators.js
    Copyright (C) 2017 Niryo
    All rights reserved.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// adds Custom Niryo One blocks + Python generators

import * as Blockly from 'blockly';
import BlocklyPy from 'blockly/python';

var niryo_one_color = '#3D4D9A';

// Interface color
var logic_color = '#00876d';
var loop_color = '#49a563';
var math_color = '#5769a1';
var list_color = '#765da1';
var variable_color = '#ad5a7e';
var function_color = '#9f5ca1';
var movement_color = '#4f87c0';
var io_color = '#c05150';
var tool_color = '#bf964b';
var utility_color = '#bead76';
var vision_color = '#546e7a';
var conveyor_color = '#00838f';

// Color object for vision
//TODO Should be in a class
const g_color_values = {
  COLOR_RED: 'RED',
  COLOR_GREEN: 'GREEN',
  COLOR_BLUE: 'BLUE',
  COLOR_ANY: 'ANY'
};

// Shape object for vision
//TODO Should be in a class
const g_shape_values = {
  SHAPE_SQUARE: 'SQUARE',
  SHAPE_CIRCLE: 'CIRCLE',
  SHAPE_ANY: 'ANY'
};

/*
 *  Blocks definition
 */

// Movement
Blockly.Blocks['niryo_one_connect'] = {
  init: function () {
    this.appendDummyInput().appendField('IP Address');
    this.appendDummyInput()
      .appendField(new Blockly.FieldNumber(10, 0, 255, 0), 'ip_0')
      .appendField('.')
      .appendField(new Blockly.FieldNumber(10, 0, 255, 0), 'ip_1')
      .appendField('.')
      .appendField(new Blockly.FieldNumber(10, 0, 255, 0), 'ip_2')
      .appendField('.')
      .appendField(new Blockly.FieldNumber(10, 0, 255, 0), 'ip_3');
    this.appendStatementInput('DO');
    this.setInputsInline(true);
    this.setPreviousStatement(false, null);
    this.setNextStatement(false, null);
    this.setColour(function_color);
    this.setTooltip('Connect to the robot and disconnects after the execution');
    this.setHelpUrl('');
  }
};
Blockly.Blocks['niryo_one_move_joints'] = {
  init: function () {
    this.appendDummyInput().appendField('Move Joints');
    this.appendDummyInput()
      .appendField('j1')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'JOINTS_1'
      )
      .appendField('j2')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'JOINTS_2'
      )
      .appendField('j3')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'JOINTS_3'
      )
      .appendField('j4')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'JOINTS_4'
      )
      .appendField('j5')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'JOINTS_5'
      )
      .appendField('j6')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'JOINTS_6'
      );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('Give all 6 joints to move the robot');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_move_pose'] = {
  init: function () {
    this.appendDummyInput().appendField('Move Pose');
    this.appendDummyInput()
      .appendField('x')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'POSE_X'
      )
      .appendField('y')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'POSE_Y'
      )
      .appendField('z')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'POSE_Z'
      )
      .appendField('roll')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'POSE_ROLL'
      )
      .appendField('pitch')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'POSE_PITCH'
      )
      .appendField('yaw')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'POSE_YAW'
      );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_shift_pose'] = {
  init: function () {
    this.appendDummyInput().appendField('Shift');
    this.appendDummyInput()
      .appendField(
        new Blockly.FieldDropdown([
          ['pos. x', '0'],
          ['pos. y', '1'],
          ['pos. z', '2'],
          ['rot. x', '3'],
          ['rot. y', '4'],
          ['rot. z', '5']
        ]),
        'SHIFT_POSE_AXIS'
      )
      .appendField('by')
      .appendField(
        new Blockly.FieldNumber(0, -Infinity, Infinity, 0.001),
        'SHIFT_POSE_VALUE'
      );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_set_arm_max_speed'] = {
  init: function () {
    this.appendValueInput('SET_ARM_MAX_SPEED')
      .setCheck('Number')
      .appendField('Set Arm max. speed to');
    this.appendDummyInput().appendField('%');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_calibrate_auto'] = {
  init: function () {
    this.appendDummyInput().appendField('Calibrate motors (auto)');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip(
      'Will auto calibrate motors. If already calibrated, will do nothing.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_calibrate_manual'] = {
  init: function () {
    this.appendDummyInput().appendField('Calibrate motors (manual)');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip(
      'Will manually calibrate motors (robot needs to be in home position). If already calibrated, will do nothing.'
    );
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_activate_learning_mode'] = {
  init: function () {
    this.appendDummyInput()
      .appendField(
        new Blockly.FieldDropdown([
          ['Activate', '1'],
          ['Deactivate', '0']
        ]),
        'LEARNING_MODE_VALUE'
      )
      .appendField('learning mode');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_joint'] = {
  init: function () {
    this.appendDummyInput().appendField('Joints');
    this.appendValueInput('j1').setCheck('Number').appendField('j1');
    this.appendValueInput('j2').setCheck('Number').appendField('j2');
    this.appendValueInput('j3').setCheck('Number').appendField('j3');
    this.appendValueInput('j4').setCheck('Number').appendField('j4');
    this.appendValueInput('j5').setCheck('Number').appendField('j5');
    this.appendValueInput('j6').setCheck('Number').appendField('j6');
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(movement_color);
    this.setTooltip('Represents an object pose');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_move_joint_from_joint'] = {
  init: function () {
    this.appendValueInput('JOINT')
      .setCheck('niryo_one_joint')
      .appendField('Move joint');
    this.setTooltip('Move joint with an object pose given');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_move_pose_from_pose'] = {
  init: function () {
    this.appendValueInput('POSE')
      .setCheck('niryo_one_pose')
      .appendField('Move pose');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('Move pose with an object pose given');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_pose'] = {
  init: function () {
    this.appendDummyInput().appendField('Pose');
    this.appendValueInput('x').setCheck('Number').appendField('x');
    this.appendValueInput('y').setCheck('Number').appendField('y');
    this.appendValueInput('z').setCheck('Number').appendField('z');
    this.appendValueInput('roll').setCheck('Number').appendField('roll');
    this.appendValueInput('pitch').setCheck('Number').appendField('pitch');
    this.appendValueInput('yaw').setCheck('Number').appendField('yaw');
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setColour(movement_color);
    this.setTooltip('Represents an object pose');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_move_pose_from_pose'] = {
  init: function () {
    this.appendValueInput('POSE')
      .setCheck('niryo_one_pose')
      .appendField('Move pose');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('Move pose with an object pose given');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_pick_from_pose'] = {
  init: function () {
    this.appendValueInput('POSE')
      .setCheck('niryo_one_pose')
      .appendField('Pick from pose');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('Pick an object at a pose given');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_place_from_pose'] = {
  init: function () {
    this.appendValueInput('POSE')
      .setCheck('niryo_one_pose')
      .appendField('Place from pose');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(movement_color);
    this.setTooltip('Place an object at a pose given');
    this.setHelpUrl('');
  }
};

// I/O

Blockly.Blocks['niryo_one_gpio_select'] = {
  init: function () {
    this.appendDummyInput().appendField(
      new Blockly.FieldDropdown([
        ['1A', 'GPIO_1A'],
        ['1B', 'GPIO_1B'],
        ['1C', 'GPIO_1C'],
        ['2A', 'GPIO_2A'],
        ['2B', 'GPIO_2B'],
        ['2C', 'GPIO_2C']
      ]),
      'GPIO_SELECT'
    );
    this.setOutput(true, 'niryo_one_gpio_select');
    this.setColour(io_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_set_pin_mode'] = {
  init: function () {
    this.appendValueInput('SET_PIN_MODE_PIN')
      .setCheck('niryo_one_gpio_select')
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField('Set Pin');
    this.appendDummyInput()
      .appendField('to mode')
      .appendField(
        new Blockly.FieldDropdown([
          ['INPUT', 'PIN_MODE_INPUT'],
          ['OUTPUT', 'PIN_MODE_OUTPUT']
        ]),
        'PIN_MODE_SELECT'
      );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(io_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_digital_write'] = {
  init: function () {
    this.appendValueInput('DIGITAL_WRITE_PIN')
      .setCheck('niryo_one_gpio_select')
      .appendField('Set Pin');
    this.appendDummyInput()
      .appendField('to state')
      .appendField(
        new Blockly.FieldDropdown([
          ['HIGH', 'PIN_HIGH'],
          ['LOW', 'PIN_LOW']
        ]),
        'PIN_WRITE_SELECT'
      );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(io_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_digital_read'] = {
  init: function () {
    this.appendValueInput('DIGITAL_READ_PIN')
      .setCheck('niryo_one_gpio_select')
      .appendField('Get Pin');
    this.appendDummyInput().appendField('state');
    this.setInputsInline(true);
    this.setOutput(true, 'niryo_one_gpio_state');
    this.setColour(io_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_gpio_state'] = {
  init: function () {
    this.appendDummyInput()
      .appendField('state')
      .appendField(
        new Blockly.FieldDropdown([
          ['HIGH', 'PIN_HIGH'],
          ['LOW', 'PIN_LOW']
        ]),
        'GPIO_STATE_SELECT'
      );
    this.setOutput(true, 'niryo_one_gpio_state');
    this.setColour(io_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_sw_select'] = {
  init: function () {
    this.appendDummyInput().appendField(
      new Blockly.FieldDropdown([
        ['SW1', 'SW_1'],
        ['SW2', 'SW_2']
      ]),
      'SW_SELECT'
    );
    this.setOutput(true, 'niryo_one_sw_select');
    this.setColour(io_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_set_12v_switch'] = {
  init: function () {
    this.appendValueInput('SET_12V_SWITCH')
      .setCheck('niryo_one_sw_select')
      .appendField('Set 12V Switch');
    this.appendDummyInput()
      .appendField('to state')
      .appendField(
        new Blockly.FieldDropdown([
          ['HIGH', 'PIN_HIGH'],
          ['LOW', 'PIN_LOW']
        ]),
        'SET_12V_SWITCH_SELECT'
      );
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(io_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

// Tool

Blockly.Blocks['niryo_one_tool_select'] = {
  init: function () {
    this.appendDummyInput().appendField(
      new Blockly.FieldDropdown([
        ['Standard gripper', 'TOOL_GRIPPER_1_ID'],
        ['Large gripper', 'TOOL_GRIPPER_2_ID'],
        ['Adaptive gripper ', 'TOOL_GRIPPER_3_ID'],
        ['electromagnet 1', 'TOOL_ELECTROMAGNET_1_ID'],
        ['vacuum pump 1', 'TOOL_VACUUM_PUMP_1_ID']
      ]),
      'TOOL_SELECT'
    );
    this.setOutput(true, 'niryo_one_tool_select');
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_change_tool'] = {
  init: function () {
    this.appendValueInput('NEW_TOOL_ID')
      .setCheck('niryo_one_tool_select')
      .appendField('Change tool to');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_detach_tool'] = {
  init: function () {
    this.appendDummyInput().appendField('Detach current tool');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_open_gripper'] = {
  init: function () {
    this.appendValueInput('OPEN_GRIPPER_ID')
      .setCheck('niryo_one_tool_select')
      .appendField('Open Gripper');
    this.appendDummyInput()
      .appendField('at speed')
      .appendField(
        new Blockly.FieldDropdown([
          ['1/5', '100'],
          ['2/5', '250'],
          ['3/5', '500'],
          ['4/5', '750'],
          ['5/5', '1000']
        ]),
        'OPEN_SPEED'
      );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_close_gripper'] = {
  init: function () {
    this.appendValueInput('CLOSE_GRIPPER_ID')
      .setCheck('niryo_one_tool_select')
      .appendField('Close Gripper');
    this.appendDummyInput()
      .appendField('at speed')
      .appendField(
        new Blockly.FieldDropdown([
          ['1/5', '100'],
          ['2/5', '250'],
          ['3/5', '500'],
          ['4/5', '750'],
          ['5/5', '1000']
        ]),
        'CLOSE_SPEED'
      );
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_pull_air_vacuum_pump'] = {
  init: function () {
    this.appendValueInput('PULL_AIR_VACUUM_PUMP_ID')
      .setCheck('niryo_one_tool_select')
      .appendField('Pull air with Vacuum Pump');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_push_air_vacuum_pump'] = {
  init: function () {
    this.appendValueInput('PUSH_AIR_VACUUM_PUMP_ID')
      .setCheck('niryo_one_tool_select')
      .appendField('Push air with Vacuum Pump');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_setup_electromagnet'] = {
  init: function () {
    this.appendValueInput('SETUP_ELECTROMAGNET_ID')
      .setCheck('niryo_one_tool_select')
      .appendField('Setup Electromagnet');
    this.appendValueInput('SETUP_ELECTROMAGNET_PIN')
      .setCheck('niryo_one_gpio_select')
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField('with pin');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_activate_electromagnet'] = {
  init: function () {
    this.appendValueInput('ACTIVATE_ELECTROMAGNET_ID')
      .setCheck('niryo_one_tool_select')
      .appendField('Activate Electromagnet');
    this.appendValueInput('ACTIVATE_ELECTROMAGNET_PIN')
      .setCheck('niryo_one_gpio_select')
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField('with pin');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_deactivate_electromagnet'] = {
  init: function () {
    this.appendValueInput('DEACTIVATE_ELECTROMAGNET_ID')
      .setCheck('niryo_one_tool_select')
      .appendField('Deactivate Electromagnet');
    this.appendValueInput('DEACTIVATE_ELECTROMAGNET_PIN')
      .setCheck('niryo_one_gpio_select')
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField('with pin');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(tool_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

// Utility

Blockly.Blocks['niryo_one_sleep'] = {
  init: function () {
    this.appendValueInput('SLEEP_TIME')
      .setCheck('Number')
      .appendField('Wait for ');
    this.appendDummyInput().appendField('seconds');
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(utility_color);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_comment'] = {
  init: function () {
    this.appendDummyInput()
      .appendField('Comment :')
      .appendField(new Blockly.FieldTextInput(''), 'COMMENT_TEXT');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(utility_color);
    this.setTooltip('This block will not be executed.');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['niryo_one_break_point'] = {
  init: function () {
    this.appendDummyInput().appendField('Break Point');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(utility_color);
    this.setTooltip(
      "Stop the execution of the program. Press 'Play' to resume."
    );
    this.setHelpUrl('');
  }
};

// Vision

Blockly.Blocks['niryo_one_vision_color'] = {
  init: function () {
    this.appendDummyInput()
      .appendField('Color')
      .appendField(
        new Blockly.FieldDropdown([
          ['RED', 'COLOR_RED'],
          ['GREEN', 'COLOR_GREEN'],
          ['BLUE', 'COLOR_BLUE'],
          ['ANY', 'COLOR_ANY']
        ]),
        'COLOR_SELECT'
      );
    this.setOutput(true, 'niryo_one_vision_color');
    this.setColour(vision_color);
    this.setTooltip("Color object (must be used with Vision's blocks)");
  }
};

Blockly.Blocks['niryo_one_vision_shape'] = {
  init: function () {
    this.appendDummyInput()
      .appendField('Shape')
      .appendField(
        new Blockly.FieldDropdown([
          ['SQUARE', 'SHAPE_SQUARE'],
          ['CIRCLE', 'SHAPE_CIRCLE'],
          ['OBJECT', 'SHAPE_ANY']
        ]),
        'SHAPE_SELECT'
      );
    this.setOutput(true, 'niryo_one_vision_shape');
    this.setColour(vision_color);
    this.setTooltip("Shape object (must be used with Vision's blocks)");
  }
};

Blockly.Blocks['niryo_one_vision_pick'] = {
  init: function () {
    this.appendValueInput('COLOR_SWITCH')
      .setCheck('niryo_one_vision_color')
      .appendField('Vision pick');

    this.appendValueInput('SHAPE_SWITCH').setCheck('niryo_one_vision_shape');
    this.appendDummyInput().appendField('in workspace');

    this.appendValueInput('WORKSPACE_NAME').setCheck('String');

    this.appendValueInput('HEIGHT_OFFSET')
      .setCheck('Number')
      .appendField('with height offset (mm)');

    this.setOutput(true, 'Boolean');
    this.setColour(vision_color);
    this.setHelpUrl('');
    this.setTooltip(
      'Pick an object of SHAPE / COLOR  given, with gripper close position at HEIGHT_OFFSET cm.'
    );
    this.setInputsInline(false);
  }
};

Blockly.Blocks['niryo_one_vision_is_object_detected'] = {
  init: function () {
    this.appendValueInput('COLOR_SWITCH')
      .setCheck('niryo_one_vision_color')
      .appendField('Is object detected');

    this.appendValueInput('SHAPE_SWITCH').setCheck('niryo_one_vision_shape');
    this.appendDummyInput().appendField('in workspace');

    this.appendValueInput('WORKSPACE_NAME').setCheck('String');

    this.setOutput(true, 'Boolean');
    this.setColour(vision_color);
    this.setHelpUrl('');
    this.setTooltip(
      'Detect is there is an object of SHAPE / COLOR in the WORKSPACE given.'
    );
    this.setInputsInline(false);
  }
};

// Conveyor

Blockly.Blocks['niryo_one_conveyor_models'] = {
  init: function () {
    this.appendDummyInput().appendField(
      new Blockly.FieldDropdown([
        ['Conveyor 1', 'CONVEYOR_1'],
        ['Conveyor 2', 'CONVEYOR_2']
      ]),
      'CONVEYOR_SELECT'
    );
    this.setOutput(true, 'niryo_one_conveyor_models');

    this.setColour(conveyor_color);
    this.setHelpUrl('');
    this.setTooltip('Conveyors available with Niryo One.');
  }
};

Blockly.Blocks['niryo_one_conveyor_use'] = {
  init: function () {
    this.appendValueInput('CONVEYOR_SWITCH')
      .setCheck('niryo_one_conveyor_models')
      .appendField('Use conveyor:');

    this.setColour(conveyor_color);
    this.setHelpUrl('');
    this.setTooltip('Allow the conveyor to be controlled via Niryo One.');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
  }
};

Blockly.Blocks['niryo_one_conveyor_control'] = {
  init: function () {
    this.appendValueInput('CONVEYOR_SWITCH')
      .setCheck('niryo_one_conveyor_models')
      .appendField('Control conveyor:');

    this.appendValueInput('SPEED_PERCENT')
      .setCheck('Number')
      .appendField('with speed (%):');

    this.appendDummyInput()
      .appendField('in direction:')
      .appendField(
        new Blockly.FieldDropdown([
          ['FORWARD', '1'],
          ['BACKWARD', '-1']
        ]),
        'DIRECTION_SELECT'
      );

    this.setColour(conveyor_color);
    this.setHelpUrl('');
    this.setTooltip('Control the conveyor given.');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setInputsInline(false);
  }
};

Blockly.Blocks['niryo_one_conveyor_stop'] = {
  init: function () {
    this.appendValueInput('CONVEYOR_SWITCH')
      .setCheck('niryo_one_conveyor_models')
      .appendField('Stop conveyor');

    this.setColour(conveyor_color);
    this.setHelpUrl('');
    this.setTooltip('Stop the conveyor given.');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
  }
};

/*
 * Generators
 */

BlocklyPy['niryo_one_connect'] = function (block) {
  var ip_0 = block.getFieldValue('ip_0');
  var ip_1 = block.getFieldValue('ip_1');
  var ip_2 = block.getFieldValue('ip_2');
  var ip_3 = block.getFieldValue('ip_3');

  let branch = BlocklyPy.statementToCode(block, 'DO');
  var ip = ip_0 + '.' + ip_1 + '.' + ip_2 + '.' + ip_3;

  var code = '\nwith niryo_connect("' + ip + '") as n:\n' + branch;
  return code;
};

Blockly.Blocks['niryo_one_connect'].toplevel_init = `
from pyniryo import *

class niryo_connect():
  def __init__(self, ip):
    self.n = NiryoRobot(ip)
  def __enter__(self):
    return self.n
  def __exit__(self):
    self.n.close_connection()
`;

BlocklyPy['niryo_one_move_joints'] = function (block) {
  var number_joints_1 = block.getFieldValue('JOINTS_1');
  var number_joints_2 = block.getFieldValue('JOINTS_2');
  var number_joints_3 = block.getFieldValue('JOINTS_3');
  var number_joints_4 = block.getFieldValue('JOINTS_4');
  var number_joints_5 = block.getFieldValue('JOINTS_5');
  var number_joints_6 = block.getFieldValue('JOINTS_6');

  var code =
    'n.move_joints([' +
    number_joints_1 +
    ', ' +
    number_joints_2 +
    ', ' +
    number_joints_3 +
    ', ' +
    number_joints_4 +
    ', ' +
    number_joints_5 +
    ', ' +
    number_joints_6 +
    '])\n';
  return code;
};

BlocklyPy['niryo_one_move_pose'] = function (block) {
  var number_pose_x = block.getFieldValue('POSE_X');
  var number_pose_y = block.getFieldValue('POSE_Y');
  var number_pose_z = block.getFieldValue('POSE_Z');
  var number_pose_roll = block.getFieldValue('POSE_ROLL');
  var number_pose_pitch = block.getFieldValue('POSE_PITCH');
  var number_pose_yaw = block.getFieldValue('POSE_YAW');

  var code =
    'n.move_pose(' +
    number_pose_x +
    ', ' +
    number_pose_y +
    ', ' +
    number_pose_z +
    ', ' +
    number_pose_roll +
    ', ' +
    number_pose_pitch +
    ', ' +
    number_pose_yaw +
    ')\n';
  return code;
};

BlocklyPy['niryo_one_shift_pose'] = function (block) {
  var dropdown_shift_pose_axis = block.getFieldValue('SHIFT_POSE_AXIS');
  var number_shift_pose_value = block.getFieldValue('SHIFT_POSE_VALUE');

  var code =
    'n.shift_pose(' +
    dropdown_shift_pose_axis +
    ', ' +
    number_shift_pose_value +
    ')\n';
  return code;
};

BlocklyPy['niryo_one_set_arm_max_speed'] = function (block) {
  var value_set_arm_max_speed =
    BlocklyPy.valueToCode(block, 'SET_ARM_MAX_SPEED', BlocklyPy.ORDER_ATOMIC) ||
    '0';
  value_set_arm_max_speed = value_set_arm_max_speed
    .replace('(', '')
    .replace(')', '');
  var code = 'n.set_arm_max_velocity(' + value_set_arm_max_speed + ')\n';
  return code;
};

BlocklyPy['niryo_one_calibrate_auto'] = function (block) {
  var code = 'n.calibrate_auto()\n';
  return code;
};

BlocklyPy['niryo_one_calibrate_manual'] = function (block) {
  var code = 'n.calibrate_manual()\n';
  return code;
};

BlocklyPy['niryo_one_activate_learning_mode'] = function (block) {
  var dropdown_learning_mode_value = block.getFieldValue('LEARNING_MODE_VALUE');
  var code = 'n.activate_learning_mode(' + dropdown_learning_mode_value + ')\n';
  return code;
};

BlocklyPy['niryo_one_joint'] = function (block) {
  var value_j1 = BlocklyPy.valueToCode(block, 'j1', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_j2 = BlocklyPy.valueToCode(block, 'j2', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_j3 = BlocklyPy.valueToCode(block, 'j3', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_j4 = BlocklyPy.valueToCode(block, 'j4', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_j5 = BlocklyPy.valueToCode(block, 'j5', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_j6 = BlocklyPy.valueToCode(block, 'j6', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');

  var code =
    '[' +
    value_j1 +
    ', ' +
    value_j2 +
    ', ' +
    value_j3 +
    ', ' +
    value_j4 +
    ', ' +
    value_j5 +
    ', ' +
    value_j6 +
    ']';
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_move_joint_from_joint'] = function (block) {
  // Position object
  var value_joint = BlocklyPy.valueToCode(
    block,
    'JOINT',
    BlocklyPy.ORDER_ATOMIC
  );
  value_joint = value_joint.replace('(', '').replace(')', '');

  var code = 'n.move_joints(' + value_joint + ')\n';
  return code;
};

BlocklyPy['niryo_one_pose'] = function (block) {
  var value_x = BlocklyPy.valueToCode(block, 'x', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_y = BlocklyPy.valueToCode(block, 'y', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_z = BlocklyPy.valueToCode(block, 'z', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_roll = BlocklyPy.valueToCode(block, 'roll', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');
  var value_pitch = BlocklyPy.valueToCode(
    block,
    'pitch',
    BlocklyPy.ORDER_ATOMIC
  )
    .replace('(', '')
    .replace(')', '');
  var value_yaw = BlocklyPy.valueToCode(block, 'yaw', BlocklyPy.ORDER_ATOMIC)
    .replace('(', '')
    .replace(')', '');

  var code =
    '[' +
    value_x +
    ', ' +
    value_y +
    ', ' +
    value_z +
    ', ' +
    value_roll +
    ', ' +
    value_pitch +
    ', ' +
    value_yaw +
    ']';
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_move_pose_from_pose'] = function (block) {
  // Position object
  var value_pose = BlocklyPy.valueToCode(block, 'POSE', BlocklyPy.ORDER_ATOMIC);
  value_pose = value_pose.replace('(', '').replace(')', '');

  var code = 'n.move_pose(*' + value_pose + ')\n';
  return code;
};

BlocklyPy['niryo_one_pick_from_pose'] = function (block) {
  // Position object
  var value_pose = BlocklyPy.valueToCode(block, 'POSE', BlocklyPy.ORDER_ATOMIC);
  value_pose = value_pose.replace('(', '').replace(')', '');

  var code = 'n.pick_from_pose(*' + value_pose + ')\n';
  return code;
};

BlocklyPy['niryo_one_place_from_pose'] = function (block) {
  // Position object
  var value_pose = BlocklyPy.valueToCode(block, 'POSE', BlocklyPy.ORDER_ATOMIC);
  value_pose = value_pose.replace('(', '').replace(')', '');

  var code = 'n.place_from_pose(*' + value_pose + ')\n';
  return code;
};

// I/O

BlocklyPy['niryo_one_gpio_state'] = function (block) {
  var dropdown_gpio_state_select = block.getFieldValue('GPIO_STATE_SELECT');
  var code = dropdown_gpio_state_select;
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_set_pin_mode'] = function (block) {
  var value_pin =
    BlocklyPy.valueToCode(block, 'SET_PIN_MODE_PIN', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  value_pin = value_pin.replace('(', '').replace(')', '');
  var dropdown_pin_mode_select = block.getFieldValue('PIN_MODE_SELECT');
  var code =
    'n.pin_mode(' + value_pin + ', ' + dropdown_pin_mode_select + ')\n';
  return code;
};

BlocklyPy['niryo_one_digital_write'] = function (block) {
  var value_pin =
    BlocklyPy.valueToCode(block, 'DIGITAL_WRITE_PIN', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  value_pin = value_pin.replace('(', '').replace(')', '');
  var dropdown_pin_write_select = block.getFieldValue('PIN_WRITE_SELECT');
  var code =
    'n.digital_write(' + value_pin + ', ' + dropdown_pin_write_select + ')\n';
  return code;
};

BlocklyPy['niryo_one_digital_read'] = function (block) {
  var value_pin =
    BlocklyPy.valueToCode(block, 'DIGITAL_READ_PIN', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  value_pin = value_pin.replace('(', '').replace(')', '');
  var code = 'n.digital_read(' + value_pin + ')';
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_gpio_select'] = function (block) {
  var dropdown_gpio_select = block.getFieldValue('GPIO_SELECT');
  var code = dropdown_gpio_select;
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_sw_select'] = function (block) {
  var dropdown_sw_select = block.getFieldValue('SW_SELECT');
  var code = dropdown_sw_select;
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_set_12v_switch'] = function (block) {
  var value_pin =
    BlocklyPy.valueToCode(block, 'SET_12V_SWITCH', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  value_pin = value_pin.replace('(', '').replace(')', '');
  var dropdown_set_12v_switch_select = block.getFieldValue(
    'SET_12V_SWITCH_SELECT'
  );
  var code =
    'n.digital_write(' +
    value_pin +
    ', ' +
    dropdown_set_12v_switch_select +
    ')\n';
  return code;
};

// Tool

BlocklyPy['niryo_one_tool_select'] = function (block) {
  var dropdown_tool_select = block.getFieldValue('TOOL_SELECT');
  var code = dropdown_tool_select;
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_change_tool'] = function (block) {
  var value_tool_name =
    BlocklyPy.valueToCode(block, 'NEW_TOOL_ID', BlocklyPy.ORDER_ATOMIC) ||
    '(TOOL_NONE)';
  value_tool_name = value_tool_name.replace('(', '').replace(')', '');
  var code = 'n.change_tool(' + value_tool_name + ')\n';
  return code;
};

BlocklyPy['niryo_one_detach_tool'] = function (block) {
  var code = 'n.change_tool(0)\n';
  return code;
};

BlocklyPy['niryo_one_open_gripper'] = function (block) {
  var value_gripper_id =
    BlocklyPy.valueToCode(block, 'OPEN_GRIPPER_ID', BlocklyPy.ORDER_ATOMIC) ||
    '(TOOL_NONE)';
  value_gripper_id = value_gripper_id.replace('(', '').replace(')', '');
  var number_open_speed = block.getFieldValue('OPEN_SPEED');
  var code =
    'n.open_gripper(' + value_gripper_id + ', ' + number_open_speed + ')\n';
  return code;
};

BlocklyPy['niryo_one_close_gripper'] = function (block) {
  var value_gripper_id =
    BlocklyPy.valueToCode(block, 'CLOSE_GRIPPER_ID', BlocklyPy.ORDER_ATOMIC) ||
    '(TOOL_NONE)';
  value_gripper_id = value_gripper_id.replace('(', '').replace(')', '');
  var number_close_speed = block.getFieldValue('CLOSE_SPEED');
  var code =
    'n.close_gripper(' + value_gripper_id + ', ' + number_close_speed + ')\n';
  return code;
};

BlocklyPy['niryo_one_pull_air_vacuum_pump'] = function (block) {
  var value_vacuum_pump_id =
    BlocklyPy.valueToCode(
      block,
      'PULL_AIR_VACUUM_PUMP_ID',
      BlocklyPy.ORDER_ATOMIC
    ) || '(TOOL_NONE)';
  value_vacuum_pump_id = value_vacuum_pump_id.replace('(', '').replace(')', '');
  var code = 'n.pull_air_vacuum_pump(' + value_vacuum_pump_id + ')\n';
  return code;
};

BlocklyPy['niryo_one_push_air_vacuum_pump'] = function (block) {
  var value_vacuum_pump_id =
    BlocklyPy.valueToCode(
      block,
      'PUSH_AIR_VACUUM_PUMP_ID',
      BlocklyPy.ORDER_ATOMIC
    ) || '(TOOL_NONE)';
  value_vacuum_pump_id = value_vacuum_pump_id.replace('(', '').replace(')', '');
  var code = 'n.push_air_vacuum_pump(' + value_vacuum_pump_id + ')\n';
  return code;
};

BlocklyPy['niryo_one_setup_electromagnet'] = function (block) {
  var value_electromagnet_id =
    BlocklyPy.valueToCode(
      block,
      'SETUP_ELECTROMAGNET_ID',
      BlocklyPy.ORDER_ATOMIC
    ) || '(TOOL_NONE)';
  value_electromagnet_id = value_electromagnet_id
    .replace('(', '')
    .replace(')', '');
  var value_electromagnet_pin =
    BlocklyPy.valueToCode(
      block,
      'SETUP_ELECTROMAGNET_PIN',
      BlocklyPy.ORDER_ATOMIC
    ) || '(0)';
  value_electromagnet_pin = value_electromagnet_pin
    .replace('(', '')
    .replace(')', '');
  var code =
    'n.setup_electromagnet(' +
    value_electromagnet_id +
    ', ' +
    value_electromagnet_pin +
    ')\n';
  return code;
};

BlocklyPy['niryo_one_activate_electromagnet'] = function (block) {
  var value_electromagnet_id =
    BlocklyPy.valueToCode(
      block,
      'ACTIVATE_ELECTROMAGNET_ID',
      BlocklyPy.ORDER_ATOMIC
    ) || '(TOOL_NONE)';
  value_electromagnet_id = value_electromagnet_id
    .replace('(', '')
    .replace(')', '');
  var value_electromagnet_pin =
    BlocklyPy.valueToCode(
      block,
      'ACTIVATE_ELECTROMAGNET_PIN',
      BlocklyPy.ORDER_ATOMIC
    ) || '(0)';
  value_electromagnet_pin = value_electromagnet_pin
    .replace('(', '')
    .replace(')', '');
  var code =
    'n.activate_electromagnet(' +
    value_electromagnet_id +
    ', ' +
    value_electromagnet_pin +
    ')\n';
  return code;
};

BlocklyPy['niryo_one_deactivate_electromagnet'] = function (block) {
  var value_electromagnet_id =
    BlocklyPy.valueToCode(
      block,
      'DEACTIVATE_ELECTROMAGNET_ID',
      BlocklyPy.ORDER_ATOMIC
    ) || '(TOOL_NONE)';
  value_electromagnet_id = value_electromagnet_id
    .replace('(', '')
    .replace(')', '');
  var value_electromagnet_pin =
    BlocklyPy.valueToCode(
      block,
      'DEACTIVATE_ELECTROMAGNET_PIN',
      BlocklyPy.ORDER_ATOMIC
    ) || '(0)';
  value_electromagnet_pin = value_electromagnet_pin
    .replace('(', '')
    .replace(')', '');
  var code =
    'n.deactivate_electromagnet(' +
    value_electromagnet_id +
    ', ' +
    value_electromagnet_pin +
    ')\n';
  return code;
};

// Utility

BlocklyPy['niryo_one_sleep'] = function (block) {
  var value_sleep_time =
    BlocklyPy.valueToCode(block, 'SLEEP_TIME', BlocklyPy.ORDER_ATOMIC) || '0';
  value_sleep_time = value_sleep_time.replace('(', '').replace(')', '');
  var code = 'n.wait(' + value_sleep_time + ')\n';
  return code;
};

BlocklyPy['niryo_one_comment'] = function (block) {
  var text_comment_text = block.getFieldValue('COMMENT_TEXT');
  var code = ' #' + text_comment_text + '\n';
  return code;
};

BlocklyPy['niryo_one_break_point'] = function (block) {
  var code = 'n.break_point()\n';
  return code;
};

// Vision

BlocklyPy['niryo_one_vision_color'] = function (block) {
  var dropdown_color_select = block.getFieldValue('COLOR_SELECT');
  var code = dropdown_color_select;
  code = '"' + g_color_values[code] + '"';
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_vision_shape'] = function (block) {
  var dropdown_shape_select = block.getFieldValue('SHAPE_SELECT');
  var code = dropdown_shape_select;
  code = '"' + g_shape_values[code] + '"';
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_vision_pick'] = function (block) {
  // Color (int) value (see g_shape_values at top of this file)
  var value_color =
    BlocklyPy.valueToCode(block, 'COLOR_SWITCH', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  value_color = value_color.replace('(', '').replace(')', '');

  // Shape (int) value (see g_shape_values at top of this file)
  var value_shape =
    BlocklyPy.valueToCode(block, 'SHAPE_SWITCH', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  value_shape = value_shape.replace('(', '').replace(')', '');

  // Name of workspace
  var workspace_name =
    BlocklyPy.valueToCode(block, 'WORKSPACE_NAME', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  workspace_name = workspace_name.replace('(', '').replace(')', '');

  // Height in centimeter
  var height_offset =
    BlocklyPy.valueToCode(block, 'HEIGHT_OFFSET', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  height_offset = height_offset.replace('(', '').replace(')', '');

  var code =
    'n.vision_pick(' +
    workspace_name +
    ', float(' +
    height_offset +
    ')/1000, ' +
    value_shape +
    ', ' +
    value_color +
    ')[0]';
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_vision_is_object_detected'] = function (block) {
  // Color (int) value (see g_shape_values at top of this file)
  var value_color =
    BlocklyPy.valueToCode(block, 'COLOR_SWITCH', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  value_color = value_color.replace('(', '').replace(')', '');

  // Shape (int) value (see g_shape_values at top of this file)
  var value_shape =
    BlocklyPy.valueToCode(block, 'SHAPE_SWITCH', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  value_shape = value_shape.replace('(', '').replace(')', '');

  // Name of workspace
  var workspace_name =
    BlocklyPy.valueToCode(block, 'WORKSPACE_NAME', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  workspace_name = workspace_name.replace('(', '').replace(')', '');

  var code =
    'n.detect_object(' +
    workspace_name +
    ', ' +
    value_shape +
    ', ' +
    value_color +
    ')[0]';
  return [code, BlocklyPy.ORDER_NONE];
};

// Conveyor

BlocklyPy['niryo_one_conveyor_models'] = function (block) {
  const conveyor_id_map = {
    CONVEYOR_1: 6,
    CONVEYOR_2: 7
  };
  var conveyor_model_id = block.getFieldValue('CONVEYOR_SELECT');
  var code = conveyor_id_map[conveyor_model_id];
  return [code, BlocklyPy.ORDER_NONE];
};

BlocklyPy['niryo_one_conveyor_use'] = function (block) {
  var conveyor_id =
    BlocklyPy.valueToCode(block, 'CONVEYOR_SWITCH', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  conveyor_id = conveyor_id.replace('(', '').replace(')', '');
  var code = 'n.set_conveyor(' + conveyor_id + ', True)\n';
  return code;
};

BlocklyPy['niryo_one_conveyor_control'] = function (block) {
  var conveyor_id =
    BlocklyPy.valueToCode(block, 'CONVEYOR_SWITCH', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  conveyor_id = conveyor_id.replace('(', '').replace(')', '');
  var speed_percent =
    BlocklyPy.valueToCode(block, 'SPEED_PERCENT', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  speed_percent = speed_percent.replace('(', '').replace(')', '');
  var direction = block.getFieldValue('DIRECTION_SELECT');
  var code =
    'n.control_conveyor(' +
    conveyor_id +
    ', True, ' +
    speed_percent +
    ', ' +
    direction +
    ')\n';
  return code;
};

BlocklyPy['niryo_one_conveyor_stop'] = function (block) {
  var conveyor_id =
    BlocklyPy.valueToCode(block, 'CONVEYOR_SWITCH', BlocklyPy.ORDER_ATOMIC) ||
    '(0)';
  conveyor_id = conveyor_id.replace('(', '').replace(')', '');
  var code = 'n.control_conveyor(' + conveyor_id + ', False, 0, 1)\n';
  return code;
};

// Creating a toolbox containing all the main (default) blocks.
const TOOLBOX = {
  kind: 'categoryToolbox',
  contents: [
    {
      kind: 'category',
      name: 'Logic',
      colour: '210',
      contents: [
        {
          kind: 'block',
          type: 'controls_if'
        },
        {
          kind: 'BLOCK',
          type: 'logic_compare'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_operation"></block>',
          type: 'logic_operation'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_negate"></block>',
          type: 'logic_negate'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_boolean"></block>',
          type: 'logic_boolean'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_null"></block>',
          type: 'logic_null'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="logic_ternary"></block>',
          type: 'logic_ternary'
        }
      ]
    },
    {
      kind: 'category',
      name: 'Loops',
      colour: '120',
      contents: [
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="controls_repeat_ext">\n          <value name="TIMES">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'controls_repeat_ext'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="controls_whileUntil"></block>',
          type: 'controls_whileUntil'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="controls_for">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n          <value name="BY">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'controls_for'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="controls_forEach"></block>',
          type: 'controls_forEach'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="controls_flow_statements"></block>',
          type: 'controls_flow_statements'
        }
      ]
    },
    {
      kind: 'CATEGORY',
      name: 'Math',
      colour: '230',
      contents: [
        {
          kind: 'BLOCK',
          blockxml: '<block type="math_number"></block>',
          type: 'math_number'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_arithmetic">\n          <value name="A">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="B">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_arithmetic'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_single">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">9</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_single'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_trig">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">45</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_trig'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="math_constant"></block>',
          type: 'math_constant'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_number_property">\n          <value name="NUMBER_TO_CHECK">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_number_property'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_change">\n          <value name="DELTA">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_change'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_round">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">3.1</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_round'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="math_on_list"></block>',
          type: 'math_on_list'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_modulo">\n          <value name="DIVIDEND">\n            <shadow type="math_number">\n              <field name="NUM">64</field>\n            </shadow>\n          </value>\n          <value name="DIVISOR">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_modulo'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_constrain">\n          <value name="VALUE">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="LOW">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="HIGH">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_constrain'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="math_random_int">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'math_random_int'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="math_random_float"></block>',
          type: 'math_random_float'
        }
      ]
    },
    {
      kind: 'CATEGORY',
      name: 'Text',
      colour: '160',
      contents: [
        {
          kind: 'BLOCK',
          blockxml: '<block type="text"></block>',
          type: 'text'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="text_join"></block>',
          type: 'text_join'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_append">\n          <value name="TEXT">\n            <shadow type="text"></shadow>\n          </value>\n        </block>',
          type: 'text_append'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_length">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_length'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_isEmpty">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT"></field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_isEmpty'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n          <value name="FIND">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_indexOf'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_charAt">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
          type: 'text_charAt'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_getSubstring">\n          <value name="STRING">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
          type: 'text_getSubstring'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_changeCase">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_changeCase'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_trim">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_trim'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_print">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_print'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="text_prompt_ext">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'text_prompt_ext'
        }
      ]
    },
    {
      kind: 'CATEGORY',
      name: 'Lists',
      colour: '260',
      contents: [
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_create_with">\n          <mutation items="0"></mutation>\n        </block>',
          type: 'lists_create_with'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="lists_create_with"></block>',
          type: 'lists_create_with'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_repeat">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">5</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'lists_repeat'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="lists_length"></block>',
          type: 'lists_length'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="lists_isEmpty"></block>',
          type: 'lists_isEmpty'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
          type: 'lists_indexOf'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_getIndex">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
          type: 'lists_getIndex'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_setIndex">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
          type: 'lists_setIndex'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_getSublist">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
          type: 'lists_getSublist'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="lists_split">\n          <value name="DELIM">\n            <shadow type="text">\n              <field name="TEXT">,</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'lists_split'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="lists_sort"></block>',
          type: 'lists_sort'
        }
      ]
    },
    {
      kind: 'CATEGORY',
      name: 'Color',
      colour: '20',
      contents: [
        {
          kind: 'BLOCK',
          blockxml: '<block type="colour_picker"></block>',
          type: 'colour_picker'
        },
        {
          kind: 'BLOCK',
          blockxml: '<block type="colour_random"></block>',
          type: 'colour_random'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="colour_rgb">\n          <value name="RED">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n          <value name="GREEN">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="BLUE">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'colour_rgb'
        },
        {
          kind: 'BLOCK',
          blockxml:
            '<block type="colour_blend">\n          <value name="COLOUR1">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#ff0000</field>\n            </shadow>\n          </value>\n          <value name="COLOUR2">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#3333ff</field>\n            </shadow>\n          </value>\n          <value name="RATIO">\n            <shadow type="math_number">\n              <field name="NUM">0.5</field>\n            </shadow>\n          </value>\n        </block>',
          type: 'colour_blend'
        }
      ]
    },
    {
      kind: 'SEP'
    },
    {
      kind: 'CATEGORY',
      colour: '330',
      custom: 'VARIABLE',
      name: 'Variables'
    },
    {
      kind: 'CATEGORY',
      colour: '290',
      custom: 'PROCEDURE',
      name: 'Functions'
    },
    {
      kind: 'SEP'
    },
    {
      kind: 'CATEGORY',
      colour: '210',
      name: 'Niryo',
      contents: [
        {
          kind: 'BLOCK',
          type: 'niryo_one_connect'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_move_joints'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_move_pose'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_shift_pose'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_set_arm_max_speed'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_calibrate_auto'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_calibrate_manual'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_activate_learning_mode'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_joint'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_move_joint_from_joint'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_move_pose_from_pose'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_pose'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_move_pose_from_pose'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_pick_from_pose'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_place_from_pose'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_gpio_select'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_set_pin_mode'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_digital_write'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_digital_read'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_gpio_state'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_sw_select'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_set_12v_switch'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_tool_select'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_change_tool'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_detach_tool'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_open_gripper'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_close_gripper'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_pull_air_vacuum_pump'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_push_air_vacuum_pump'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_setup_electromagnet'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_activate_electromagnet'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_deactivate_electromagnet'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_sleep'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_comment'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_break_point'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_vision_color'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_vision_shape'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_vision_pick'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_vision_is_object_detected'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_conveyor_models'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_conveyor_use'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_conveyor_control'
        },
        {
          kind: 'BLOCK',
          type: 'niryo_one_conveyor_stop'
        }
      ]
    }
  ]
};

const BlocklyNiryo = {
  Blocks: Blockly.Blocks,
  Generator: BlocklyPy,
  Toolbox: TOOLBOX
};

export default BlocklyNiryo;
