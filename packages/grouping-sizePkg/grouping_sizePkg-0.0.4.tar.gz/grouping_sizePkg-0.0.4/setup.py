import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grouping_sizePkg",
    version="0.0.4",
    author="Example Author",
    author_email="author@example.com",
    description="Grouping for cmf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pstrito/grouping_sizePip.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)