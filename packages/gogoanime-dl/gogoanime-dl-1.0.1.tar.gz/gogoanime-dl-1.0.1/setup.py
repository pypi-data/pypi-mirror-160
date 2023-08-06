"""
@author: AuraMoon55
@contact: garganshul553@gmail.com
@license: MIT License, see LICENSE file
Copyright (C) 2022
"""


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '1.0.1'


with open('README.md') as f:
    long_description = f.read()


setup(
    name='gogoanime-dl',
    version=version,

    author='AuraMoon55',

    author_email='garganshul553@gmail.com',
    url='https://github.com/AuraMoon55/',

    description='GoGoAnime file downloader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',

    packages=['gogoanime'],
    install_requires=['requests', 'bs4', 'selenium'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    zip_safe=False,
    python_requires="~=3.7"
)
