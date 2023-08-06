from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Link Slot Gacor'
long_description = open('README.md').read()

# Setting up
setup(
    name="link-slot-gacor",
    version=VERSION,
    author="HIGGSGO",
    author_email="<higgsgo@bonanzabon.click>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['higgsgo','link slot gacor','slot gacor','slot online','slot gacor ternama','judi online','togel online','agen slot online','bandar slot online','judi slot online','slot online terbaik','slot online terpercaya'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
