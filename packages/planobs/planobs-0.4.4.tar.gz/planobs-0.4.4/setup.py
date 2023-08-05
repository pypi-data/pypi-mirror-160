import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="planobs",
    version="0.4.4",
    author="Simeon Reusch",
    author_email="simeon.reusch@desy.de",
    description="Plan observations with the Zwicky Transient Facility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD (3-clause)",
    keywords="astronomy astrophysics",
    url="https://github.com/simeonreusch/planobs",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8.0",
    package_data={
        "planobs": [
            "data/*.csv",
            "data/references/*.csv",
        ]
    },
    install_requires=[
        "astroplan>=0.7",
        "astropy",
        "coveralls",
        "geopandas",
        "pandas",
        "penquins",
        "lxml",
        "matplotlib",
        "shapely",
        "tqdm",
        "ztfquery",
    ],
    extras_require={"full": ["flask", "slack", "slackeventsapi"]},
)
