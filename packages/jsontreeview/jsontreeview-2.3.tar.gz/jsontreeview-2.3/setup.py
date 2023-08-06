# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="jsontreeview",  # Required

    version="2.3",  # Required

    description="A simple python program for viewing JSON data more clearly",  # Optional

    long_description=long_description,  # Optional

    long_description_content_type="text/markdown",  # Optional (see note above)

    author="tk",  # Optional
    
    packages=find_packages(),  # Required

    python_requires=">=3.7, <4",

    project_urls={  # Optional
        "Source": "https://github.com/tksoftw/JsonTreeView"
    },
)
