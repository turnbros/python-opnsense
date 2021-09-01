from distutils.core import setup
setup(
  name = 'python-opnsense',
  packages = ['opnsense_api'],
  version = '0.1.4',
  license='apache-2.0',
  description = 'A python library that interacts with an Opnsense API',
  author = 'Dylan Turnbull',
  author_email = 'dylanturn@gmail.com',
  url = 'https://github.com/turnbros/python-opnsense',
  download_url = 'https://github.com/turnbros/python-opnsense/archive/refs/tags/0.1.1.tar.gz',
  keywords = ['turnbros', 'opnsense'],
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent'
  ],
)