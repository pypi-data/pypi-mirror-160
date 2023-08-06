from setuptools import setup
long_description = open("README.md").read()

setup(name="colourfulprint",
version="1.5",
description="Colourfulprint for Rainbow print without extra newline character(\n).",
long_description=long_description,
long_description_content_type='text/markdown',
author="NISHANT",
url="https://github.com/Nishant2009/colourfulprint",
scripts=["colourfulprint"],
classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
], )
