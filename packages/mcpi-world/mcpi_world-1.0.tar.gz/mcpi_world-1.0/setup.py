from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcpi_world",
    version="1.0",
    author = "The StevePi Organization",
    maintainer = "LEHAtupointow",
    maintainer_email = "leha2@tuxfamily.org",
    description="level.dat editor for MCPE versions => 0.8.1",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=["amulet_nbt"],
    packages=["mcpi_world"],
    package_dir={"mcpi_world":"src"}
)
