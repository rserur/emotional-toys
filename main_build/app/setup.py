from setuptools import setup

OPTIONS = {'argv_emulation': True}
DATA_FILES= []

setup(
	app = ['__main__.py'],
	options = {'py2app': OPTIONS},
	data_files = DATA_FILES,
	)