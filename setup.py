from setuptools import setup, find_packages

setup(
    name="fut_card_creator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Pillow>=8.0.0",  # Required for image processing
        "requests>=2.0.0",  # Required for API calls
        "fuzzywuzzy[speedup]>=0.18.0",  # Required for fuzzy string matching
        "python-Levenshtein>=0.12.0",  # Required for fuzzywuzzy speedup
    ],
    author="AngelFire",
    description="A package that allows you to create custom FUT cards",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/AngelFireLA/FutCardCreator",
    python_requires='>=3.6',
)
