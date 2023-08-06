#!/usr/bin/python3
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='toolky',
    version='0.1.0',
    author='Keyu Tian',
    author_email='tiankeyu.00@gmail.com',
    description='tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/keyu-research/toolky',
    packages=setuptools.find_packages(),
    platforms=['all'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pkg_resources',
        # 'pathos'
    ],
    entry_points={
        'console_scripts': [
            'sea = toolky.search:main'
        ]
    }
)
