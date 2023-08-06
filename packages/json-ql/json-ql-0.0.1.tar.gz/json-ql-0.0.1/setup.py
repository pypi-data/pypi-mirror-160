import setuptools


def read(fname):
    """Return file content."""
    with open(fname) as f:
        content = f.read()

    return content


description = "A plug-n-play package fetch test data from WPT and parse for specific keys"
try:
    long_description = read("README.MD")
except IOError:
    long_description = description

setuptools.setup(
    name="json-ql",
    package=["json-ql"],
    version="0.0.1",
    author="Bharat Sinha",
    author_email="bharat.sinha.2307@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bharat23/json-ql",
    packages=setuptools.find_packages(),
    license="MIT",
    keywords=["json", "ql", "lookup", "dict"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    install_requires=[
    ],
    python_requires=">=3.6",
)
