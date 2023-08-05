from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="armstrong_asmita",
    version="1.0.0",
    description="Asmita tarar",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Akshay311/armstrong",
    author="Asmita Tarar",
    author_email="asmitatarar@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["package"],
    include_package_data=True,
)