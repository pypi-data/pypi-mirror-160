# setup.py
from setuptools import setup, find_packages
import sys
import os
sys.path.append(os.path.dirname(__file__))
import versioneer

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name="url_text_module",
    author="Urban Risk Lab",
    author_email="url_googleai@mit.edu",
    description="Text Module of REACT",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/react76/url-text-module",
    project_urls={
        "Bug Tracker": "https://gitlab.com/react76/url-text-module/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    package_dir={"": "src"},
    python_requires=">=3.7",
    packages=find_packages(where="src")
)