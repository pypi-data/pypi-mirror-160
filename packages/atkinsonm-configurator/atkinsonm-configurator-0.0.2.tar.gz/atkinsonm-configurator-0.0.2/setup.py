# setup.py

from setuptools import setup, find_packages
from io import open
from os import path
import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs
                    if 'git+' not in x]

setup(
    name="atkinsonm-configurator",
    description="A simple configuration management tool designed for performing administrative actions on Linux servers",
    version="0.0.2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "atkinsonm-configurator = configurator.cli:cli"
        ]
    },
    author="Mike Atkinson",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/atkinsonm/slack-ops-challenge",
    dependency_links=dependency_links,
    author_email='m.g.atkinson@outlook.com',
)
