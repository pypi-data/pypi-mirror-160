from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dcargs",
    version="0.1.10",
    description="Strongly typed, zero-effort CLIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/brentyi/dcargs",
    author="brentyi",
    author_email="brentyi@berkeley.edu",
    license="MIT",
    packages=find_packages(),
    package_data={"dcargs": ["py.typed"]},
    python_requires=">=3.7",
    install_requires=[
        "docstring_parser",
        "typing_extensions>=4.3.0",
        "pyyaml",
        "termcolor",
        "backports.cached-property; python_version < '3.8.0'",
    ],
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
            "omegaconf",
            "attrs",
            "torch",
        ],
        "type-checking": [
            "mypy",
            "pyright",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
