#!/usr/bin/env python3

from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    return long_description


def requirements():
    requirements_list = []

    with open("requirements.txt") as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list


packages = find_packages()
requirements = requirements()


def main():
    setup(
        name="se-exporter",
        version="1.0.0",
        author="Akim Faskhutdinov",
        author_email="akimstrong@yandex.ru",
        license="MIT",
        description="Space Engineers server metrics exporter for Prometheus",
        long_description=readme(),
        long_description_content_type="text/markdown",
        url="https://github.com/akimrx/space-engineers-exporter",
        keywords=["space engineers exporter", "prometheus", "space engineers server"],
        platforms=["osx", "linux"],
        packages=packages,
        install_requrements=requirements,
        include_package_data=True,
        python_requires=">=3.6",
        entry_points={
            "console_scripts": [
                "se-exporter=main.main"
            ]
        },
        zip_safe=False
    )


if __name__ == "__main__":
    main()
