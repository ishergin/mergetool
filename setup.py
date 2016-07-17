from os.path import join, dirname
from setuptools import setup
import sys

setup(
    name='mergetool',
    version='0.1',
    scripts=['gitmerge'],
    packages=['mergetool'],
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=['argparse', 'gitpython'],
    license='',
    author='Igor Shergin',
    author_email='ishergin@gmail.com',
    description='Git branch merge tool'
)
