#!/bin/bash
# install script for packages

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail
set +x


# if you want to use a virtual env
# python3 -m venv env
# source env/bin/activate

pip install flask

pip install -q -U google-generativeai

pip install opencv-python


