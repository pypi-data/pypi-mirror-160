from setuptools import setup, find_packages
import os

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + "/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

requirements = ["<arcgis> >= <2.0.1>"]
requirements_dev = []

setup(
    name="bentoncounty_gistools",
    version="0.0.8",
    author="Erik Rose",
    author_email="erik.w.rose@gmail.com",
    description="Mapping tools for Benton County Community Development, Oregon",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/crumplecup/bentoncounty_gistools/",
    packages=find_packages(),
    install_requires=install_requires,
    tests_requires=requirements_dev,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
