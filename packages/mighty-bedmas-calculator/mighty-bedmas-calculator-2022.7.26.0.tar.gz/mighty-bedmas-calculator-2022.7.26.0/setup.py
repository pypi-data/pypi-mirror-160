"""Setup file for Odyssey Settings."""

from os.path import dirname, join
from pathlib import Path

from setuptools import find_packages, setup

GITHUB_URL = "https://github.com/jdboisvert/mightly-bedmas-calculator"
VERSION = "2022.7.26.0"


def read(fname):
    """Read content of a file and return as a string."""
    return Path(join(dirname(__file__), fname)).read_text()


def get_requirements():
    """Return requirements with loose version restrictions."""
    return read("requirements.txt").replace("==", ">=").split("\n")


setup(
    name="mighty-bedmas-calculator",
    version=VERSION,
    license="MIT License",
    url=GITHUB_URL,
    download_url=f"{GITHUB_URL}/archive/refs/tags/v{VERSION}.zip",
    project_urls={"Repository": GITHUB_URL, "Bug Reports": f"{GITHUB_URL}/issues"},
    author="""Jeffrey Boisvert""",
    author_email="info.jeffreyboisvert@gmail.com",
    description="""Calculate string infix expressions following BEDMAS.""",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=get_requirements(),
    test_suite="tests",
    keywords=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.2.5", "pytest-xdist==2.5.0"],
    python_requires=">=3.8.0",
    entry_points={
        "console_scripts": [
            "mighty-bedmas-calculator=mighty_bedmas_calculator._cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
