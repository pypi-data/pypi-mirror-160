import os
import setuptools

with open("/home/runner/termux-1/rembgpy/README.md", "r") as fh:
    long_description = fh.read()


with open('/home/runner/termux-1/rembgpy/requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="rembgpy",
    version="1.0.1",
    author="jiroawesome",
    description="A simple python api wrapper for remove.bg.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiroawesome/rembgpy",
    project_urls={
        "Bug Tracker": "https://github.com/jiroawesome/rembgpy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={'': ['**/*']},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=required
)