from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Encrypting and Decrypting data'
LONG_DESCRIPTION = 'A package that allows you to encrypt and decrypt data using the best algorithms to date.'

# Setting up
setup(
    name="data_cipher",
    version=VERSION,
    author="Dronikon (Nikita Derevyankin)",
    author_email="<dronikosha@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pycryptodome'],
    keywords=['python', 'encrypt', 'decrypt', 'aes', 'blowfish'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)