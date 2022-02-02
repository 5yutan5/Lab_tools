# DIYHV

GUI for high voltage controller

## Installation

You can install a freezing app from Releases.

## Get started

```terminal
cd DIYHV
python -m diy_hv
```

## Usage

### How to send command

1. Press the Connect button to connect to the device.
1. Select **Static** or **Dynamic** menu.
1. Select voltage and frequency.
1. Press the Send Command button to send the command.

### How to register user commands

1. Select Setting menu in menu bar.
1. Open file dialog with the **Setting** > **Register user file**.
1. Select Setting file to register additional command(The default commands will be reset).

Example of a command settings file. You need to use json.

```json
{
    "stop": "s",
    "static": [
        {
            "command": "a",
            "voltage": 1
        },
        {
            "command": "b",
            "voltage": 2
        },
        {
            "command": "c",
            "voltage": 3
        },
        {
            "command": "d",
            "voltage": 4
        }
    ],
    "dynamic": [
        {
            "command": "d",
            "voltage": 1,
            "frequency": 1
        },
        {
            "command": "e",
            "voltage": 1,
            "frequency": 5
        },
        {
            "command": "f",
            "voltage": 1,
            "frequency": 10
        }
    ]
}

```
