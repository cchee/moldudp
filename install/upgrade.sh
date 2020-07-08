#!/bin/bash
version=${1}

pip3 uninstall -y moldudp
python3 -m pip install -i https://test.pypi.org/simple/ moldudp==$version
