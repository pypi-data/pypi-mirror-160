from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dip-python",
    packages=find_packages(),

    version="0.1.1",

    license="MIT",

    python_requires=">=3.6",
    install_requires=['numpy'],

    author="RinYixi",
    author_email="hayashi0241@gmail.com",

    url="https://github.com/R1nY1x1/dippy",

    description="Digital Image Processing in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="dippy",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
