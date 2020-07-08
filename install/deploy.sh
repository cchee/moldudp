#!/bin/bash
repo=${1:-testpypi}

rm -rf build dist moldudp_codec.egg-info
python3 setup.py sdist bdist_wheel
if [ "${repo}" == "pypi" ]; then
  python3 -m twine upload --verbose dist/*
else
  python3 -m twine upload --repository $repo --verbose dist/*
fi
