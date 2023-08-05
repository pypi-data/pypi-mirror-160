import setuptools 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ShortPaw",
    version="0.0.1",
    description="A CLI Tools for ShortPaw",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://shortpaw.herokuapp.com",
    author="NoobScience",
    author_email="noobscience123@gmail.com",
    license="MIT",
    project_urls={
        "Author WebSite" : "https://newtoallofthis123.github.io/About",
        "Bug Tracker": "https://github.com/newtoallofthis123/shortpaw/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=["rich", "requests"],
    entry_points={
        "console_scripts": [
            "shortpaw=shortpaw.__main__:main",
        ]
    },
)