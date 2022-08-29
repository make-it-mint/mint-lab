#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#create venv if it does not exist
test -d "$SCRIPT_DIR/.mint_venv" \
    || { \
        python -m venv "$SCRIPT_DIR/.mint_venv" \
        && source "$SCRIPT_DIR/.mint_venv/bin/activate" \
        && pip3 install -r "$SCRIPT_DIR/requirements.txt"; \
    }
#For development purposes this file is different and creates a specific python environment for testing on Linux

#Check all requirements are met and run
pip3 install -r "$SCRIPT_DIR/requirements.txt" \
&& python3 "$SCRIPT_DIR/tools/flashing_tool/flashing_tool.py"