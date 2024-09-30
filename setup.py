"""
Setup configuration for the fast-api-kube package.

This module uses setuptools to configure the distribution package for the
`fast-api-kube` project. It specifies metadata such as the package name,
version, description, author details, and licensing information. Additionally,
it includes the required dependencies and package details for distribution.

Functions:
    readme(): Reads and returns the contents of the README.md file.
"""

from setuptools import setup


def readme():
    """
    Read and return the contents of the README.md file.

    Returns:
        str: The contents of the README.md file as a string.
    """
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="fast-api-kube",
    version="0.1",
    description="fast-api-kube",
    url="https://github.com/maher-naija-pro/fast-api-kube",
    author="maher naija",
    author_email="maher.naija@gmail.Com",
    license="MIT",
    packages=["src"],
    install_requires=[
        "",
    ],
    zip_safe=False,
)
