"""
Setup configuration for the fast-api-kube package.

This module uses setuptools to configure the distribution package for the
`fast-api-kube` project. It specifies metadata such as the package name,
version, description, author details, and licensing information. Additionally,
it includes the required dependencies and package details for distribution.

"""

from setuptools import setup

setup(
    name="fast-api-kube",
    version="0.2",
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
