"""Setup script for the Holy Cow Image Gen package."""
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Holy_Cow_Image_Gen",
    version="0.1",
    author="Kabyik",
    packages=find_packages(),
    install_requires = requirements,
)