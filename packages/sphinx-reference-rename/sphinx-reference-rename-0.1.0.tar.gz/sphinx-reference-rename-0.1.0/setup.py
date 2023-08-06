from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='sphinx-reference-rename',
    version='0.1.0',
    description='rename sphinx references',
    long_description=long_description,
    url='https://github.com/brenns10/sphinx-reference-rename',
    author='Stephen Brennan',
    author_email='stephen@brennan.io',
    license='GPL v2',
    packages=['sphinx_reference_rename'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Framework :: Sphinx :: Extension',
    ],
    keywords='sphinx reference rename',
)
