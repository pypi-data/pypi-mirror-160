#py -m twine upload dist/* -p 5014348112nagara -u mongran --verbose
#py setup.py sdist bdist_wheel
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usdkrw", # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="mongranflower@hotmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    package_dir={"":'forex'},
    packages=setuptools.find_packages(where='forex'),
    py_modules=["usdkrw"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)