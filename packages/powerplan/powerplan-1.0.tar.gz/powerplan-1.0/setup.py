from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0'
DESCRIPTION = 'Get windows powerplan scheme'

setup(
    name="powerplan",
    version=VERSION,
    author="Temal",
    author_email="contact@temal.cf",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'windows', 'powerplan'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)