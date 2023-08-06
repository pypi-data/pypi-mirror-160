import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='textmail',
    version='1.0',
    scripts=['textmail'],
    author="Andrew Stein",
    author_email="stein.andrew.01@gmail.com",
    description="A tool for sending text messages via email",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndrewCPU/textmail",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)