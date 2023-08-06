from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Gobuubstackmodel",
    version="0.3",
    description="Personal Python lib for used for EDA's and train ML models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Enrique Revuelta Garcia",
    author_email="enrique.revuelta@enriquerevueltagarcia.com",
    url="https://github.com/Gobuub/Gobuub-Stack-Model-Lib",
    packages=find_packages(),
    scripts=[]
)
