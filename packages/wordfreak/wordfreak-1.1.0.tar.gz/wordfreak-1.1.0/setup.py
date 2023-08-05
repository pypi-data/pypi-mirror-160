import setuptools

with open("README.md") as f:
    readMe = f.read()

with open("LICENSE") as f:
    license = f.read()

setuptools.setup(
    name="wordfreak",
    version="1.1.0",
    author="Joey Greco",
    author_email="joeyagreco@gmail.com",
    description="Word Freak is a Python library that extracts word frequencies from files.",
    long_description_content_type="text/markdown",
    long_description=readMe,
    license=license,
    packages=setuptools.find_packages(exclude=("test", "docs")),
    install_requires=["PyPDF2",
                      "docx2txt",
                      "setuptools"]
)
