import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="G5encode",
    version="0.0.6",
    author="Example Author",
    author_email="Glitch5@hotmail.com",
    description="This is to encrypt tools or files or words",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Team-G5/G5encode",
    project_urls={
        "Bug Tracker": "https://github.com/Team-G5/G5encode/issues/1",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "seconde"},
    packages=setuptools.find_packages(where="seconde"),
    python_requires=">=3.6",
)