
from setuptools import setup, find_packages
from setuptools import Command
import sys, subprocess


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        try:
            subprocess.call(['docker', '-v'])
        except OSError:
            print("Docker is required to run the functional tests.")
            sys.exit(1)

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call([sys.executable, '-m', 'tests.functional_tests'])


setup(
    name = 'fabric-package-management',
    version = '0.1',
    description='A collection of fabric tasks for package management',

    author='Andrew Starr-Bochicchio',
    author_email='a.starr.b@gmail.com',

    packages = find_packages(),
    install_requires = ['fabric'],
    cmdclass = {'test': TestCommand}
)
