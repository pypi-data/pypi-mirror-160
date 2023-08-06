import os
import codecs
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A basic detect package'
LONG_DESCRIPTION = "This is a python package to detect face on image"

# Setting Up

setup(
    name="pydata_vision",
    version=VERSION,
    author="Data Vision (Maruf Ibragimov)",
    author_email="ifacevision@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'face_recognition'],
    keywords=['python', 'image', 'detect', 'face'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)