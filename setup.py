from distutils.core import setup

setup (
  name = 'Blog',
  version = '0.1',
  author = 'Thomas Lant',
  author_email = 'thomas.lant@gmail.com',
  packages = ['blog'],
  scripts = ['bin/start-blog'],
  license = 'LICENSE.txt',
  description = 'Not a blog',
  long_description = open('README.txt').read(),
)
