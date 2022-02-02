# Electromechanical-Tensile-Tester

Electromechanical tensile test software for Stretchable Conductive Materials.

## Requirements

- [Python 3.7+](https://www.python.org/downloads/)
- PySide6, PyQt6, PyQt5 or PySide2

## Installation

Run following commands in your terminal. Or you can install freezing package in [Releases](https://github.com/5yutan5/Lab_tools/releases).

- MacOS & Linux

    ```Terminal
    cd Electromechanical-Tensile-Tester
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install ./pyAutoLab ./pyautolab-hioki ./pyautolab-optosigma ./pyautolab-loadcell
    pip install PyQt6
    ```

- Windows

    ```Terminal
    cd Electromechanical-Tensile-Tester
    python -m venv .venv
    .venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install .\pyAutoLab .\pyautolab-hioki .\pyautolab-optosigma .\pyautolab-loadcell
    pip install PyQt6
    ```

## Usage

Run following commands.

```Terminal
pyautolab
```
