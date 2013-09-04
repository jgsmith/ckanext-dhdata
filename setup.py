from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-dhdata',
	version=version,
	description="Theme and extensions specific to DHData.Org",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='James Smith',
	author_email='admin@dhdata.org',
	url='http://www.dhdata.org/',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.dhdata'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	dhdata=ckanext.dhdata.plugins:DHDataPlugin
	""",
)
