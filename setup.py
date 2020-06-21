import io
import os
from shutil import rmtree
import sys

from setuptools import Command, find_packages, setup


# Package meta-data.
NAME = 'advego-antiplagiat-api'
DESCRIPTION = 'Неофициальный клиент для работы с сервисом антиплагиата от advego.com.'
URL = 'https://github.com/V-ampire/advego-antiplagiat-api'
EMAIL = 'webjob010@gmail.com'
AUTHOR = 'V-ampire'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = None

REQUIRED = ['requests',]

# ------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

try:
	with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as fp:
		long_description = '\n' + fp.read()
except FileNotFoundError:
	long_description = DESCRIPTION

about = {}

if not VERSION:
	package_name = 'antiplagiat'
	with open(os.path.join(here, package_name, '__version__.py')) as fp:
		exec(fp.read(), about)
else:
	about['__version__'] = VERSION


class UploadCommand(Command):
	"""Support setup.py upload."""

	description = 'Build and publish the package.'
	user_options = []

	@staticmethod
	def status(s):
		"""Prints things in bold."""
		print('\033[1m{0}\033[0m'.format(s))

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		try:
			self.status('Removing previous builds…')
			rmtree(os.path.join(here, 'dist'))
		except OSError:
			pass

		self.status('Building Source and Wheel distribution…')
		os.system(f'{sys.executable} setup.py sdist bdist_wheel')

		self.status('Uploading the package to PyPI via Twine…')
		os.system('twine upload dist/*')

		self.status('Pushing git tags…')
		os.system(f'git tag v{about["__version__"]}')
		os.system('git push --tags')

		sys.exit()


setup(
	name=NAME,
	version=about['__version__'],
	description=DESCRIPTION,
	long_description=long_description,
	long_description_content_type='text/markdown',
	author=AUTHOR,
	author_email=EMAIL,
	python_requires=REQUIRES_PYTHON,
	url=URL,
	packages=find_packages(exclude=['tests']),
	install_requires=REQUIRED,
	include_package_data=True,
	license='MIT',
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Operating System :: Unix',
		'Topic :: Software Development :: Libraries',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: Implementation :: CPython',
	],
	keywords = ['antiplagiat', 'advego', 'api', 'wrapper', 'sdk', 'integration', 'v-ampire', 'lib'],
	zip_safe = False,
	cmdclass = {'upload': UploadCommand},
)