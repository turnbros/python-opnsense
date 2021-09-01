from distutils.core import setup
setup(
  name = 'python-opnsense',
  packages = ['opnsense_api'],
  version = '0.1',
  license='apache-2.0',
  description = 'A python library that interacts with an Opnsense API',
  author = 'Dylan Turnbull',
  author_email = 'dylanturn@gmail.com',
  url = 'https://github.com/turnbros/python-opnsense',
  download_url = 'https://github.com/turnbros/python-opnsense/v_01.tar.gz',
  keywords = ['turnbros', 'opnsense'],
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent'
  ],
)