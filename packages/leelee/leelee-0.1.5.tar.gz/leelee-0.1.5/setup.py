import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leelee", ## 소문자 영단어
    version="0.1.5", ##
    author="leelee", ## ex) Sunkyeong Lee
    author_email="dlrlduq94@gmail.com", ##
    description="PUT THE PACKAGE DESCRIPTION", ##
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rlduqdl94", ##
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)