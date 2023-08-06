#!/usr/bin/env python
import datetime

from setuptools import setup, find_packages

readme = open("README.md").read()

VERSION = "0.1.7"

requirements = [
    "onnx",
    "numpy",
    'tabulate'
]

setup(
    # Metadata
    name="onnx-tool",
    version=VERSION,
    author="Luo Yu",
    author_email="luoyu888888@gmail.com",
    url="https://github.com/ThanatosShinji/onnx-tool",
    description="A tool for ONNX model's shape inference and MACs(FLOPs) counting.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    # Package info
    packages=find_packages(),
    #
    zip_safe=True,
    install_requires=requirements,
    # Classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)