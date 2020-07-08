from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()


setup(
    name='moldudp_codec',
    version='0.0.8',
    description='A simple library to decode/encode MoldUDP64 bytearray/packet',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cchee/moldudp_codec',
    author='Chester Chee',
    author_email='chester.chee@gmail.com',
    packages=find_packages(),
    python_requires='>=3.0',
    project_urls={
        'Bug Reports': 'https://github.com/cchee/moldudp_codec/issues',
        'Source': 'https://github.com/cchee/moldudp_codec/',
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='moldudp nasdaq development',
    license=open('LICENSE').read(),
    platform='any',
)
