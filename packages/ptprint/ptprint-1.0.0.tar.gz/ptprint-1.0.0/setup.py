from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ptprint',
  version='1.0.0',
  description='Pretty Terminal print library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Prepakis Georgios',
  author_email='prepakis.geo@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='prettyprint', 
  packages=find_packages(),
  install_requires=[''] 
)