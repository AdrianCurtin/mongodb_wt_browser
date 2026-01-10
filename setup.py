"""
Setup script for MongoDB WiredTiger Browser
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='mongodb-wt-browser',
    version='1.0.0',
    author='Adrian Curtin',
    description='A tool to open MongoDB WiredTiger backups and export tables',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AdrianCurtin/mongodb_wt_browser',
    py_modules=['wt_browser', 'cli'],
    install_requires=[
        'wiredtiger>=11.2.0',
        'click>=8.1.7',
    ],
    entry_points={
        'console_scripts': [
            'mongodb-wt-browser=cli:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Database',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    keywords='mongodb wiredtiger backup export database',
)
