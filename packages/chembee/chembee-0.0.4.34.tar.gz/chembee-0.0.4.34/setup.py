import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name="chembee",
    version="0.0.4.34",
    author="Julian M. Kleber",
    author_email="juilian.kleber@sail.black",
    description="Package for using Machine Learning and AI for designing chemicals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.codeberg/cap_jmk/chembee",
    packages=setuptools.find_packages(include=["chembee*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
