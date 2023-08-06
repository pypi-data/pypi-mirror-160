from setuptools import setup, find_packages

VERSION = "v2.0.0"

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="pyrostep",
    version=VERSION,
    description="A step handler library for pyrogram framework",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="aWolver",
    url="https://github.com/aWolver/pyrostep",
    packages=find_packages(exclude=["example"]),
    requires=["pyrogram"],
    keywords=["pyrogram", "step handler", "pyrogram helper", "pyrostep", "pyrogram connection"],
    license="GPLv2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ]
)
