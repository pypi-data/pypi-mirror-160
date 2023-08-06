import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="doc-wizard",
    version="1.0.1",
    description="A prospective zmq-i2c server replacement",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/jtrielof/doc-wizard.git",
    author="Jonathan Trieloff",
    author_email="j.trieloff@cern.ch",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["doc_wizard"],
    include_package_data=True,
    install_requires=['typing', 'click'],
    entry_points={
        "console_scripts": [
            "doc-wizard=doc_wizard.__main__:parseOpts",
        ]
    },
)
