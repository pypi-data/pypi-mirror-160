from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Get data from youtube with individous'

# Setting up
setup(
    name="individous-wrapper",
    version=VERSION,
    author="Jonathan Krüger",
    author_email="<jonathan@mag-roboter.de>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'bs4'],
    keywords=['python', 'youtube', 'individous', 'wrapper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)
