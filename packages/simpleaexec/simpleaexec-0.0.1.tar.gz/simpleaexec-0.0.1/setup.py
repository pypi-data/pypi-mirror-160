from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Simple async. executor.'

# Setting up
setup(
	name="simpleaexec",
	version=VERSION,
	author="mqchinee",
	description=DESCRIPTION,
	packages=find_packages(),
	install_requires=['io', 'contextlib', 'aioconsole'],
	keywords=['python', 'aexec', 'simple'],
	classifiers=[
		"Development Status :: 1 - Planning",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Operating System :: Unix",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)