from setuptools import setup, find_packages

setup(
    name="fut_card_creator",
    version="1.3.3",
    packages=find_packages(),
    install_requires=[
        "Pillow>=8.0.0",
        "requests>=2.0.0",
        "fuzzywuzzy[speedup]>=0.18.0",
        "python-Levenshtein>=0.12.0",
    ],
    author="AngelFire",
    description="A package that allows you to create custom FUT cards",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/AngelFireLA/FutCardCreator",
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        '': ['images/card_templates/*.png', 'images/nation_cache/*.png', 'images/club_logo_cache/*.png', 'fonts/*.otf'],
    },
)
