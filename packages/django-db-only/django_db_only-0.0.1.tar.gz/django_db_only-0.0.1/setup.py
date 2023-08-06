from setuptools import setup, find_packages

EXCLUDE_FROM_PACKAGES = [
	'django_db_only.conf.project_template',
]

setup(
	name='django_db_only',
	version='0.0.1',
	description='Django models as standalone app.',
	long_description='Django models as standalone app.',
	author='Abror Qodirov',
	author_email='splayerme@gmail.com',
	packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
	entry_points={'console_scripts': [
		'django_db_only = django_db_only:execute_from_command_line',
	]},
	url='http://github.com/abrorbekuz/django_db_only',
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python",
		"License :: OSI Approved :: Python Software Foundation License",
		"Development Status :: 3 - Alpha",
		"Operating System :: OS Independent",
		"Framework :: Django",
		"Intended Audience :: Developers",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
	],
	zip_safe=False,


)
