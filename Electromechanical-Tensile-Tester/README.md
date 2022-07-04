# Electromechanical-Tensile-Tester

Electromechanical tensile test software for Stretchable Conductive Materials.

[![Frontiers Paper](https://img.shields.io/badge/DOI-10.3389%2Ffrobt.2021.773056-blue)](https://doi.org/10.3389/frobt.2021.773056)

[![Frontiers Paper](https://img.shields.io/badge/DOI-10.1016%2Fj.ohx.2022.e00287-blue)](https://doi.org/10.1016/j.ohx.2022.e00287)

## Corresponding devices

The following devices are supported.

- [LCR METER IM3536 - Hioki](https://www.hioki.com/en/products/detail/?product_key=5824)
- [2 axis Stage Controller Shot702 - OptoSigma](https://www.global-optosigma.com/en_jp/Catalogs/gno/?from=page&pnoname=SHOT-702&ccode=W9045&dcode=&gnoname=SHOT-702)
- [Translation Motorized Stages SGSP26-200(Z) - OptoSigma](https://www.global-optosigma.com/en_jp/Catalogs/gno/?from=page&pnoname=SGSP26-%28Z%29&ccode=W9016&dcode=&gnoname=SGSP26-200%28Z%29)

## Installation

Run following commands in your terminal. Or you can install freezing package in [Releases](https://github.com/5yutan5/Lab_tools/releases).

- MacOS & Linux

    ```Terminal
    cd Electromechanical-Tensile-Tester
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install ./pyAutoLab ./pyautolab-hioki ./pyautolab-optosigma ./pyautolab-loadcell
    pip install PySide6
    ```

- Windows

    ```Terminal
    cd Electromechanical-Tensile-Tester
    python -m venv .venv
    .venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install .\pyAutoLab .\pyautolab-hioki .\pyautolab-optosigma .\pyautolab-loadcell
    pip install PySide6
    ```

## Usage

Run following commands.

```Terminal
pyautolab
```
