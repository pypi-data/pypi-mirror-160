from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.2'
DESCRIPTION = 'Pulling Edgar 10Q Files'
long_description = 'Pulling Edgar 10Q Files'
# Setting up
setup(
    name="UltimateEdgarParser",
    version=VERSION,
    author="Saeed Shadkam",
    author_email="<shadkam@ualberta.ca",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'Finance', 'EDGAR', 'SEC'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)