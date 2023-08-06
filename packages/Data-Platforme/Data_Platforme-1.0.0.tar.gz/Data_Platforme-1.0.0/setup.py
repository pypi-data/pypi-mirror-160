import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Data_Platforme",
    version="1.0.0",
    author="wafa AIT DAOUD",
    author_email="aitdaoudwafa@gmail.com",
    description="Data Platforme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wafaait/DataPlateform",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)