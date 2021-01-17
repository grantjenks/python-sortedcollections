import pathlib
import re

from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox

        errno = tox.cmdline(self.test_args)
        exit(errno)


with open('README.rst') as reader:
    readme = reader.read()

init_text = (pathlib.Path('sortedcollections') / '__init__.py').read_text()
match = re.search(r"^__version__ = '(.+)'$", init_text, re.MULTILINE)
version = match.group(1)

setup(
    name='sortedcollections',
    version=version,
    description='Python Sorted Collections',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='http://www.grantjenks.com/docs/sortedcollections/',
    license='Apache 2.0',
    packages=['sortedcollections'],
    install_requires=['sortedcontainers'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
)
