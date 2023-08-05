import os
import setuptools

with open("/home/runner/termux-1/terminalpycolor/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terminalpycolor",
    version="1.0.2",
    author="jiroawesome",
    description="A simple python library that can be used on designing your Terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiroawesome/terminalpycolor",
    project_urls={
        "Bug Tracker": "https://github.com/jiroawesome/terminalpycolor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={'': ['**/*']},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)