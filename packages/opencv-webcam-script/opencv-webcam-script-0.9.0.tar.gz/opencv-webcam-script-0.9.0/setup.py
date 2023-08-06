#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Yifu Zeng(曾逸夫)
# Mail: zyfiy1314@163.com
# Created Time:  2022-07-26
#############################################

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="opencv-webcam-script",
    version="0.9.0",
    keywords=["opencv", "webcam"],
    description="webcam opencv script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL-3.0 Licence",
    url="https://gitee.com/CV_Lab/opencv_webcam",
    author="Yifu Zeng",
    author_email="zyfiy1314@163.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "opencv-python>=4.5.5.62",
        "PyYAML>=6.0",
        "tqdm>=4.62.3",
        "matplotlib>=3.5.1",
        "pyfiglet>=0.8.0",
        "Pillow>=8.3.2",
        "numpy>=1.22.1",
        "psutil>=5.9.0",
        "wget>=3.2",
        "rich>=12.2.0",
    ],
)
