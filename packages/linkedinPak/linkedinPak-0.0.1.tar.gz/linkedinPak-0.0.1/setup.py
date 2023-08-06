from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='linkedinPak',
  version='0.0.1',
  description='A very basic linkedin Project to follow Hr Tech Recruiters',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/asifkasi/Linkedin-Project',  
  author='Asif Kasi',
  author_email='asifkasi37@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='linkedin', 
  packages=find_packages(),
  install_requires=[''] 
)