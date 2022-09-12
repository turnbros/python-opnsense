import os
from setuptools import setup, find_packages

version = os.environ.get('BUILD_VERSION')

setup(
  name='python-opnsense',
  packages=find_packages(),
  version=version,
  license='apache-2.0',
  description='A python library that interacts with an Opnsense API',
  long_description=open('README.md', 'r').read(),
  long_description_content_type='text/markdown',
  author='Dylan Turnbull',
  author_email='dylanturn@gmail.com',
  url="https://github.com/turnbros/python-opnsense",
  download_url=f"https://github.com/turnbros/python-opnsense/releases/tag/{version}",
  keywords=['turnbros', 'opnsense'],
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent'
  ],
)
