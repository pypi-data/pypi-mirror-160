from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

setup(
    name="jacob_comeau",
    version="0.1.0",
    description="Demo library",
    author="Jacob Comeau",
    license="JAKE",
    packages=["jacob_comeau"],
    include_package_data=True,
    install_requires=["numpy", "pandas", "matplotlib", "seaborn"],
)

