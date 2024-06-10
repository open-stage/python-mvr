from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pymvr",
    version="0.2.0",
    long_description=long_description,
    description="My Virtual Rig library for Python",
    long_description_content_type="text/markdown",
    url="https://github.com/open-stage/python-mvr",
    license="MIT",
    author="vanous",
    author_email="noreply@nodomain.com",
    packages=["pymvr"],
    project_urls={
        "Source": "https://github.com/open-stage/python-mvr",
        "Changelog": "https://github.com/open-stage/python-mvr/blob/master/CHANGELOG.md",
    },
)
