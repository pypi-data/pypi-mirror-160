from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Python Wrapper for Govee API'
LONG_DESCRIPTION = 'A Python wrapper for the HTTP Govee Developer API to control Govee WiFi supported devices.'

# Setting up
setup(
    name="python-govee",
    version=VERSION,
    author="Shravan Prasanth",
    author_email="<shravanapps44@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    project_urls={
        'GitHub': 'https://github.com/shra4747/python-govee'
    },
    install_requires=['requests'],
    keywords=['python', 'govee', 'api',
              'govee home', 'govee developer', 'lights'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
