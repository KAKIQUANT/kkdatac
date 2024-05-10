from setuptools import setup, find_packages
import sys
with open("requirements.txt", "rb") as r:
    install_requires = r.read().decode("utf-8").split("\n")  
# Check OS type and add extra dependencies
if sys.platform == "win32":
    system = "windows"
elif sys.platform == "darwin":
    system = "macos"
elif sys.platform == "linux":
    system = "linux"
else:
    raise OSError("Unsupported OS")

with open(f"./extra_requirements/requirements-{system}.txt", "rb") as r:
    install_requires += r.read().decode("utf-8").split("\n")
# Load the long_description from README.md
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()
setup(
    name="kkdatac",
    version="0.0.1",
    author="Shengyang Wang",
    author_email="shengyang.wang2@dukekunshan.edu.cn",
    description="Querying data from various databases maintained by kkdatabases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KAKIQUANT/kkdatac",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Dependent",
    ],
    python_requires='>=3.10',
    install_requires=install_requires,
    project_urls={
        "Bug Tracker": "https://github.com/KAKIQUANT/kkdatac/issues",
    },
)
