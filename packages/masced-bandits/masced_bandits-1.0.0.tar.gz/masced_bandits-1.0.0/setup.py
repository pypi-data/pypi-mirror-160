import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="masced_bandits",
    version="1.0.0",
    author="Elvin Alberts",
    author_email="elvingalberts@gmail.com",
    description="multi-armed bandit policies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EGAlberts/MASCed_bandits",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)