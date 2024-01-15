import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coines_py_v3",
    version="0.1.0",
    author="Dr. Konstantin Selyunin",
    author_email="selyunin.k.v@gmail.com",
    license="MIT",
    description="Communication with BST Application Board v3 from python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/selyunin/app3.0_coines_py",
    packages=["coines_py_v3"],
    requires=["pyusb"],
    install_requires=["pyusb"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
)
