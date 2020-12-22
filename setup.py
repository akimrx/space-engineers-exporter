#!/usr/bin/env python3

from os import path
from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    return long_description

cwd = path.abspath(path.dirname(__file__))


def metadata():
    meta = {}
    with open(path.join(cwd, "se_exporter", "__version__.py"), "r") as fh:
        exec(fh.read(), meta)

    return meta


def requirements():
    requirements_list = []

    with open("requirements.txt") as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list

metadata = metadata()
readme = readme()
packages = find_packages()
requirements = requirements()


def main():
    setup(
        name="se-exporter",
        version=metadata.get("__version__"),
        author=metadata.get("__author__"),
        author_email=metadata.get("__author_email__"),
        license=metadata.get("__license__"),
        description=metadata.get("__description__"),
        long_description=readme,
        long_description_content_type="text/markdown",
        url=metadata.get("__url__"),
        keywords=["space engineers exporter", "prometheus", "space engineers server"],
        platforms=["osx", "linux"],
        packages=packages,
        classifiers = [
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Topic :: System :: Monitoring"
        ],
        install_requires=requirements,
        include_package_data=True,
        python_requires=">=3.6",
        entry_points={
            "console_scripts": [
                "se-exporter=se_exporter.main:main"
            ]
        },
        zip_safe=False
    )


if __name__ == "__main__":
    main()
