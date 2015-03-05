import dukaan

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(name='dukaan',
	version=dukaan.__version__,
	description='Local testing tool for Windows Azure Store resource providers',
	long_description=open('README.txt').read(),
	license='LICENSE.txt',
	url='https://github.com/domonkosgabor/azure-resource-provider-sdk/tree/master/tools/dukaan',
	packages=['dukaan'],
	install_requires=['clint >= 0.3.1','iso8601 >= 0.1.4','requests >= 0.14.2'],
	entry_points = {
		'console_scripts': [
			'dukaan = dukaan.dukaan:main',
        ],
    },
	classifiers=(
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		),
)