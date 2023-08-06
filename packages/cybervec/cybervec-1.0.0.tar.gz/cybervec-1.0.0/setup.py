import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cybervec",
    version="1.0.0",
    author="muzudho",
    author_email="muzudho1@gmail.com",
    description="Cyber vector notation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muzudho/cyber-vector-notation",
    project_urls={
        "Bug Tracker": "https://github.com/muzudho/cyber-vector-notation/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
