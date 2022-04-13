import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydavinci",
    version="1.0.0",
    author="Pedro Labonia",
    author_email="pedromslabonia@gmail.com",
    description="A Davinci Resolve API Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pedrolabonia/pydavinci",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),    # type: ignore
    packages=setuptools.find_packages(),
    python_requires=">=3.6.0",
)