#!/bin/bash
repo=${1:-testpypi}

rm -rf build dist moldudp_codec.egg-info
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository $repo dist/*
