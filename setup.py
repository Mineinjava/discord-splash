import setuptools
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = ''
with open('discordSplash/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setuptools.setup(
    name="discordSplash",
    version=version,


    author="Mineinjava",
    author_email="mineinjava@minein.me",
    description="An API wrapper for Discord's slash commands. Written in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mineinjava/discord-splash",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    project_urls={
        "Documentation": "https://discordsplash.readthedocs.io/",
        "Issue tracker": "https://github.com/mineinjava/discordSplash/issues",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
)
