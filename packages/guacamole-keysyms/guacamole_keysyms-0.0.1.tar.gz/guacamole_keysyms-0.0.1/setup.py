import setuptools

with open("README.md", "r") as desc:
    long_description: str = desc.read()

setuptools.setup(
    name="guacamole_keysyms",
    version="0.0.1",
    author="Ari Archer",
    author_email="ari.web.xyz@gmail.com",
    description="Guacamole protocol key mappings for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ari-web.xyz/gh/guacamole_keysyms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
