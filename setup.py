"""
Setup configuration for the fast-api-kube package.

This module uses setuptools to configure the distribution package for the
`fast-api-kube` project. It specifies metadata such as the package name,
version, description, author details, and licensing information. Additionally,
it includes the required dependencies and package details for distribution.

"""

from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fast-api-kube",
    version="0.3",
    description="fast-api-kube",
    url="https://github.com/maher-naija-pro/fast-api-kube",
    author="maher naija",
    author_email="maher.naija@gmail.Com",
    license="MIT",
    packages=["src"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "",
    ],
    zip_safe=False,
)
