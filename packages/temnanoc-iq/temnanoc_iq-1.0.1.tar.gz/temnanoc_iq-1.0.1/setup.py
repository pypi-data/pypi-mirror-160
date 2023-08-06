from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.0.1'
DESCRIPTION = "Temnanoc's iq."

# Setting up
setup(
	name="temnanoc_iq",
	version=VERSION,
	author="mqchinee",
	description=DESCRIPTION,
	packages=find_packages(),
	install_requires=[],
	keywords=['random', 'python', 'eightball'],
	classifiers=[
		"Development Status :: 1 - Planning",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Operating System :: Unix",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)