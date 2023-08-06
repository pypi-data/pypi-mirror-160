# coding=UTF-8

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='nsscurves',
    version='2022.07.22',
    author='Marcelo Horita',
    author_email='mfhorita@gmail.com.br',
    packages=['nsscurves'],
    description="Modelo Nelson Siegel Svensson.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mfhorita',
    license='MIT License',
    keywords='nss nelson siegel svensson curves',
    classifiers=[
        'License :: Freeware',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: Portuguese (Brazilian)',
        'Intended Audience :: Developers',
        'Topic :: Utilities'],
    install_requires=[
    ]

)
