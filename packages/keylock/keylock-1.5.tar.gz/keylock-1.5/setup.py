from setuptools import setup
long_description = open("README.md").read()

setup(name="keylock",
version="1.5",
description="Encryptor For Python and Bash and Decryptor for Python",
long_description=long_description,
long_description_content_type='text/markdown',
author="NISHANT",
url="https://github.com/Nishant2009/keylock",
scripts=["keylock"],
install_requires= ['requests','colourfulprint'],
classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
], )
