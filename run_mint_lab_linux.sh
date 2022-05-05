#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#For development purposes this file is different and creates a specific python environment for testing on Linux

#Check all requirements are met and run
pip3 install -r "$SCRIPT_DIR/requirements.txt" \
&& python3 "$SCRIPT_DIR/main.py"