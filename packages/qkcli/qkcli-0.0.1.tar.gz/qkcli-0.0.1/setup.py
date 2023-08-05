from setuptools import setup

with open("README.md", "r") as fh:
    long_description=fh.read()

setup(
    name="qkcli",
    url="https://github.com/dariusmaverick/qkcli",
    author="John D. Maverick",
    author_email="johndariusmaverick@gmail.com",
    version="0.0.1",
    description="Simple library to allow fast creation of CLI applications",
    py_modules=["qkcli"],
    package_dir={"": "src"},
    classifiers=[
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [ ],
    extras_require = {
        "dev": [
            "pytest >= 3.7",
        ],
    }
)

