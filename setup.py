from pathlib import Path

from setuptools import find_packages, setup

long_desc = (Path(__file__).parent / "README.md").read_text()

setup(
    name="hiosint",
    version="1.1",
    packages=find_packages(),
    author="iamosint",
    author_email="osint@iamosint.33mail.com",
    install_requires=["colorama", "aiohttp", "google"],
    description="An OSINT tool designed to gather reliable information from multiple sources.",
    include_package_data=True,
    url="https://github.com/iamosint/hiosint",
    py_modules=["hiosint"],
    entry_points={"console_scripts": ["hiosint = hiosint.cli:main"]},
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Framework :: aiohttp",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
)
