from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='spatialcdr',
  version='0.0.1',
  description='Cell type prediction in spatial transcriptomics',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Asish Kumar Swain',
  author_email='swainkasish@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='willupdate', 
  packages=find_packages(),
  install_requires=['pandas>=1.4.2',
        'numpy>=1.21.6',
        'sklearn>=1.1.0'] 
)