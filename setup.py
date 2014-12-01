import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from cmsplugin_articles import __version__


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Communications',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards',
    'Topic :: Internet :: WWW/HTTP :: Site Management',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='cmsplugin-articles',
    version=__version__,
    description='Django CMS articles management plugin',
    author='Anton Egorov',
    author_email='anton.egoroff@gmail.com',
    url='https://github.com/satyrius/cmsplugin-articles',
    license='MIT',
    long_description=open('README.rst').read(),
    classifiers=CLASSIFIERS,
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-cms',
        'Pillow',
        'beautifulsoup4',
    ],
    tests_require=['tox>=1.8'],
    cmdclass={'test': Tox},
    zip_safe=False,
)
