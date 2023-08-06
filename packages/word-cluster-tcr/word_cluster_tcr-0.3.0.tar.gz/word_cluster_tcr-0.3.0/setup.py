#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="ido hasson",
    author_email='ido.hasson.5@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="cluster cdr3 amino acid sequences",
    entry_points={
        'console_scripts': [
            'word_cluster_tcr=word_cluster_tcr.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='word_cluster_tcr',
    name='word_cluster_tcr',
    packages=find_packages(include=['word_cluster_tcr', 'word_cluster_tcr.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/idohasson/word_cluster_tcr',
    version='0.3.0',
    zip_safe=False,
)
