from setuptools import setup
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='LinAlgHelper',
  version='1.0.3',
  description='A Linear Algebra library',
  long_description=open('README.txt').read(),
  url='https://github.com/NoahPinel/LinearAlgLib',  
  author='Noah Pinel',
  author_email='noah@binaryfox.ca',
  license='MIT', 
  classifiers=classifiers,
  keywords='LinearAlgebra', 
  install_requires=[''] 
)
