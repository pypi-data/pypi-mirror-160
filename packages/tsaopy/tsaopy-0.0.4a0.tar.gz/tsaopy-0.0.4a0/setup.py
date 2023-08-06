import setuptools

with open("buildreadme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
	   name='tsaopy',
	   packages=['tsaopy'],
	   version='0.0.4a0',
	   description=('Time Series by Anharmonic Oscillators is a Python library '
		        'designed to analize time series by modelling them as '
		        'anharmonic oscillators.'),
	   long_description=long_description,
	   long_description_content_type="text/markdown",
	   url='https://tsaopy.github.io/',
	   author='Sofia A. Scozziero',
	   author_email='sgscozziero@gmail.com',
	   install_requires=['numpy','quickemcee'], 
	   classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: POSIX :: Linux",]
)