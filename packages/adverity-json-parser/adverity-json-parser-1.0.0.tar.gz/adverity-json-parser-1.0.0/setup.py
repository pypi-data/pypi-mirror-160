import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="adverity-json-parser",
    version="1.0.0",
    description="Adverity json parser is a package created to parse json files on the adverity datastreams.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/devoteamgcloud/adverity-json-parser",
    author="Nabil Lahssini | Jonas Ameye",
    author_email="nabil.lahssini@devoteam.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["adverity_json_parser"],
    install_requires=["requests"],
)