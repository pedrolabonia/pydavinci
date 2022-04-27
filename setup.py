# type: ignore
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydavinci",
    version="0.1.0",
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
    ),
    packages=setuptools.find_packages(),
    package_data={"pydavinci": ["py.typed"]},
    python_requires="==3.6.*",
    install_requires=["loguru==0.6.0", "pydantic==1.9.0"],
)
