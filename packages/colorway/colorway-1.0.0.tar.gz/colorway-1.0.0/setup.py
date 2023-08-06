from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='colorway',
    version='1.0.0',
    description='Python package to change the text color of the python console.',
    py_modules=["colorway_foreground","colorway_background"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev": [
            "pytest>=3.7",
            "check-manifest>=0.48",
            "twine>=3.8.0",
        ],
    },
    url="https://github.com/xhelphin/colorway",
    author="Jack Greenacre",
    author_email="jaxk.programmer@gmail.com",
)