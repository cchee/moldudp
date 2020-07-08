#!/bin/bash
version=${1}
repo_url=${2:-https://test.pypi.org/simple}

pip3 uninstall -y moldudp
python3 -m pip install -i $repo_url/ moldudp==$version
