from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='fabric-package-management',
    version='0.1.1',
    description='A collection of fabric tasks for package management',
    long_description=long_description,
    url='https://github.com/andrewsomething/fabric-package-management',
    download_url='https://github.com/andrewsomething/fabric-package-management/releases',
    license='MIT License (Expat)',

    author='Andrew Starr-Bochicchio',
    author_email='a.starr.b@gmail.com',

    packages=find_packages(),
    install_requires=['fabric']
)
