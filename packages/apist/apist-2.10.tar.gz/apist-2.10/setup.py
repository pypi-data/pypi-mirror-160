"""
这是上传pypi的文件
"""

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="apist",
    version="2.10",
    author="Teark",
    author_email="913355434@qq.com",
    description="apist, The best framework for api automation testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/teark/apist.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'xlutils', 'jsonpath', 'bottle'],
)
