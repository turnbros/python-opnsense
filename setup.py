from setuptools import setup, find_packages

from setuptools_scm import get_version

version = get_version(root='.', relative_to=__file__)
base_url = 'https://github.com/turnbros/python-opnsense'

setup(
  name='python-opnsense',
  packages=find_packages(),
  version=version,
  license='apache-2.0',
  description='A python library that interacts with an Opnsense API',
  author='Dylan Turnbull',
  author_email='dylanturn@gmail.com',
  url=base_url,
  download_url='{0}/releases'.format(base_url),
  keywords=['turnbros', 'opnsense'],
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent'
  ],
)