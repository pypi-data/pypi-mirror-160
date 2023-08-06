from setuptools import find_packages, setup


setup(
    name="HighJax",
    author="Daniel Dodd",
    author_email="d.dodd1@lancaster.ac.uk",
    packages=find_packages(".", exclude=["tests"]),
)
