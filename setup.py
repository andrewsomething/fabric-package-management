
from setuptools import setup, find_packages

setup(
    name = 'fabric-package-management',
    version = '0.1',
    description='A collection of fabric tasks for package management',

    author='Andrew Starr-Bochicchio',
    author_email='a.starr.b@gmail.com',

    packages = find_packages(),
    install_requires = ['fabric']
)
