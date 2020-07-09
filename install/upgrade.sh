#!/bin/bash
version=${1}
repo=${2:-testpypi}
test_repo_url=https://test.pypi.org/simple

pip3 uninstall -y moldudp
if [ "${repo}" == "pypi" ]; then
    pip3 install moldudp==$version
else
    pip3 install -i $test_repo_url/ moldudp==$version
fi
