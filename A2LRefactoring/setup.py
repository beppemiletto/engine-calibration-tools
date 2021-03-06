import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="a2lrefactor-beppemiletto", # Replace with your own username
    version="0.0.5",
    author="Beppe Miletto",
    author_email="beppe.miletto@gmail.com",
    description="A2L database refactor tool to introduce Working Points",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beppemiletto/engine-calibration-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)