

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='darklab_utils',
    version='0.0.1.dev3',
    description='Utility programms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/darklab8/darklab_utils',
    author='dd84ai',
    author_email='dd84ai@gmail.com',
    license='GNU-3',
    license_file='LICENSE',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='utils scripts',
    packages=find_packages(
        exclude=[
            'tests', 'tests.*',
        ],
    ),
    install_requires=[
    ],
    python_requires=">=3.10",
)