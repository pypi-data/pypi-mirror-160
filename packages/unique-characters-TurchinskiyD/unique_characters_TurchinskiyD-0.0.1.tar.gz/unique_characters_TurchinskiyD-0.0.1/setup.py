from setuptools import setup
from io import open

version = '0.0.1'

with open("README.md", encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='unique_characters_TurchinskiyD',
    version=version,

    author_email='turchinskiyd@gmail.com',

    description=(
        u'The module counts how many unique characters are in the string or file it is processing.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url= 'https://git.foxminded.com.ua/foxstudent101495/unique_characters',
    download_url='',

    license='MIT License, see LICENSE file',

    packages=['unique_characters_TurchinskiyD'],
    install_requires = ['argparse', 'lru_cache'],

    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)