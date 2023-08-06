import io
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tps-dashboard-utils",
    version="0.0.33",
    author="Lisa Hendry",
    author_email="lisahendry@turningpointscotland.com",
    description="Some useful utilities for building dashboards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # TODO
    url="https://github.com/losthippo/tps-dashboard-utils",
    # TODO
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)