#!/bin/bash
version=${1}

python3 -m pip uninstall moldudp-codec
python3 -m pip install -i https://test.pypi.org/simple/ moldudp-codec==$version
