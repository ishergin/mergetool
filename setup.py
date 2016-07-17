from distutils.core import setup
from os.path import join, dirname
import sys

install_requires = ['argparse', 'gitpython']

setup(
    name='mergetool',
    version='0.1',
    scripts=['gitmerge'],
    packages=['mergetool'],
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    license='',
    author='Igor Shergin',
    author_email='ishergin@gmail.com',
    description='Git branch merge tool'
)