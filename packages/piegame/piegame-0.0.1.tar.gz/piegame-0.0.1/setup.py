import os
import re
import setuptools


with open("piegame/__init__.py", "r") as fp:
    version_pat = re.compile(r"\d\.\d\.\d")
    results = version_pat.findall(fp.read())
    version = results[0] if len(results) > 0 else "0.0.1"

with open("README.md", "r") as fp:
    long_description = fp.read()

with open("requirements.txt", "r") as fp:
    requirements = fp.read().strip().split("\n")

setuptools.setup(
    name="piegame",
    version=version,
    author="Patrick Huang",
    author_email="phuang1024@gmail.com",
    description="Utilities for pygame GUI applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phuang1024/piegame",
    py_modules=["piegame"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
