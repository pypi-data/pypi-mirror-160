from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Anime Tracker package.'
LONG_DESCRIPTION = 'A package that helps to get information about any anime in any language.'

# Setting up
setup(
	name="anitrack",
	version=VERSION,
	author="mqchinee",
	description=DESCRIPTION,
	long_description_content_type="text/markdown",
	long_description=LONG_DESCRIPTION,
	packages=find_packages(),
	install_requires=['requests', 'bs4', 'urllib3', 'deep_translator', 'argparse'],
	keywords=['python', 'anime', 'track'],
	classifiers=[
		"Development Status :: 1 - Planning",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Operating System :: Unix",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)