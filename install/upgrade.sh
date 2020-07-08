#!/bin/bash
version=${1}

pip3 uninstall -y moldudp-codec
python3 -m pip install -i https://test.pypi.org/simple/ moldudp-codec==$version
