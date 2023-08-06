import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htmlit",
    version="0.1.008",
    author="Gaetan Desrues",
    author_email="gdesrues@gmail.com",
    url="https://github.com/GaetanDesrues/htmlgen",
    description="Description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["htmlit2"],  # setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
