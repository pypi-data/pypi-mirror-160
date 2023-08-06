from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="assignment-7-portfolio-generator-burrmit",
    version="1.0.0",
    description="Stock Portfolio Reports Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mitchell Burr",
    author_email="burrmit@gmail.com",
    packages=find_packages(where="portfolio"),
    python_requires=">=3.7, <4",
    install_requires=[
        "pytest",
        "requests"
    ],
    project_urls={
        "Bug Reports": "https://github.com/sheridan-python/assignment-7-portfolio-generator-burrmit/issues",
        "Source": "https://github.com/sheridan-python/assignment-7-portfolio-generator-burrmit",
    },
)
