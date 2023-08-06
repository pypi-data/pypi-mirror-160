import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="masced_bandits-EGAlberts",
    version="0.0.1",
    author="Elvin Alberts",
    author_email="elvingalberts@gmail.com",
    description="bandit algs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EGAlberts/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)