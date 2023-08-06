from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="simple_game_of_life",
    version="0.0.2",
    py_modules=["game_of_life"],
    install_requires=["numpy", "matplotlib"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ]
)
