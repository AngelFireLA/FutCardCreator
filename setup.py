# setup.py

from setuptools import setup, find_packages

setup(
    name="fut_card_creator",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # List your dependencies here
    author="AngelFire",
    description="A package that allows you to create custom FUT cards",
    #long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/AngelFireLA/FutCardCreator",
    python_requires='>=3.6',
)
