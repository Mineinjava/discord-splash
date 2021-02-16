import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discordSplash",  
    version="0.6-ALPHA",
    author="Mineinjava",
    author_email="Mineinjava@gmail.com",
    description="An API wrapper for Discord's slash commands. Written in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mineinjava/discord-splash",
    packages=["discordSplash"],
    classifiers=[
        'Programming Language :: Python :: 3'
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
