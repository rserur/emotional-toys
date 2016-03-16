from setuptools import setup
from git import Repo

OPTIONS = {'argv_emulation': True, 'iconfile': 'RAGE/art/game_icon.icns'}
DATA_FILES= [('', ['RAGE/art']), 
				('', ['RAGE/Log']), 
				('',['fonts']),
				('',['RAGE/Sounds']),]
REPO = Repo('../../')
VERSION = str(REPO.tags[-1])

setup(
	app = ['game0.py'],
  name = 'CALMS Game %(VERSION)s' % locals(),
  version = VERSION,
	options = {'py2app': OPTIONS},
	data_files = DATA_FILES,
	)