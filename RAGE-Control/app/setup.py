from setuptools import setup

OPTIONS = {'argv_emulation': True, 'iconfile': 'RAGE/art/game_icon.icns'}
DATA_FILES= [('', ['RAGE/art']), 
				('', ['RAGE/Log']), 
				('',['fonts']),
				('',['RAGE/Sounds']),]

setup(
	app = ['game0.py'],
  name = 'CALMS Game',
	options = {'py2app': OPTIONS},
	data_files = DATA_FILES,
	)