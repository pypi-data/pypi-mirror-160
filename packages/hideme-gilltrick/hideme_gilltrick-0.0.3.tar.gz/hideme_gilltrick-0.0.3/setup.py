from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Hide a file in another file'
LONG_DESCRIPTION = 'You can hide videos or images in other images or videos'

setup(
    name="hideme_gilltrick",
    version=VERSION,
    author="Gilltrick (Patrick Gillmann)",
    author_email="<mail@example.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'hide', 'files', 'videos', 'images'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)