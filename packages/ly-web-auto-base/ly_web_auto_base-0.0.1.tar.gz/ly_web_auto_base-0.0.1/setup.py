import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ly_web_auto_base",
    version="0.0.1",
    author="yjy",
    author_email="",
    description="UI自动化基类",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "selenium >= 4.1.5",
    ],
    python_requires=">=3.9",
)