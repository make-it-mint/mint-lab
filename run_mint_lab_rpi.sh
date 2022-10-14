#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


#activate venv and checkif requirements are met, if not, install required libraries
#is currently done in main python environment of Raspberry Pi, as there is no solution found yet to install PyQT5 in virtual environment
pip3 install -r "$SCRIPT_DIR/requirements_rpi.txt" \
&& python3 "$SCRIPT_DIR/main.py"