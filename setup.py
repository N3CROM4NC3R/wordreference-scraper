from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = "Scraping words from wordreference"
LONG_DESCRIPTION = "Module for scraping words and its meanings in wordreference.com"

setup(
    name="wordreference-scraper",
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    author = "Santiago Padron",
    install_requires = [
        "requests==2.26.0",
        "beautifulsoup4==4.11.1"
    ],
    package_dir = {'':'src'},
)