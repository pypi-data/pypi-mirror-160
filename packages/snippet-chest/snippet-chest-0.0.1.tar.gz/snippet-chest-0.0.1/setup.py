from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Snippets, but packaged"
LONG_DESCRIPTION = "Stuff I constantly have to google all in one place"

setup(
    name="snippet-chest",
    version=VERSION,
    author="John Nelson",
    author_email="<jbn@abreka.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)