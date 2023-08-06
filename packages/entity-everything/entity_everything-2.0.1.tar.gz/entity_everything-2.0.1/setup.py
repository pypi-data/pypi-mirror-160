import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="entity_everything",
    version="2.0.1",
    author="Daniel Rogowski",
    description="Python tool for encoding text to HTML entities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    py_modules=["entity_everything"],
    install_requires=[],
    requirements_tests=[]
)
