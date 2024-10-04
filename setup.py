"""
Setup configuration for the fast-api-kube package.

This module uses setuptools to configure the distribution package for the
`fast-api-kube` project. It specifies metadata such as the package name,
version, description, author details, and licensing information. Additionally,
it includes the required dependencies and package details for distribution.

"""

import subprocess
from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


def get_version_frogm_tag():
    """
    Retrieve the current Git tag version using `git describe --tags`.

    This function attempts to get the latest Git tag and returns it as a string.
    If the Git tag cannot be retrieved (e.g., the command fails or no tags are found),
    a fallback version of "0.0.0" is returned.

    Returns:
        str: The Git tag version as a string, or "0.0.0" if an error occurs.
    """
    try:
        version = (
            subprocess.check_output(["git", "describe", "--tags"])
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        # This will catch errors related to the git command failing
        version = "0.0.0"  # Fallback version if tag not found
    except FileNotFoundError:
        # This will catch errors if git is not installed or found
        version = "0.0.0"  # Fallback version if git is not installed
    return version


setup(
    name="fast-api-kube",
    version=get_version_frogm_tag(),
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
