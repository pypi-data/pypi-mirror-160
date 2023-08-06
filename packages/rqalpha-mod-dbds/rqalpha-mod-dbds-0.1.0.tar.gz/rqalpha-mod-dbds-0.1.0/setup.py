import sys
from setuptools import find_packages, setup

requirements = [
    'rqalpha',
    'tushare',
    'pymongo',
    'pytz',
    'pandas'
]

setup(
    name='rqalpha-mod-dbds',  # mod名
    version="0.1.0",
    description='RQAlpha Mod db as datasource',
    packages=find_packages(exclude=[]),
    author='LayeWang',
    author_email='laye0619@gmail.com',
    license='Apache License v2',
    package_data={'rqalpha-mod-dbdsls': ['*.*']},
    url='',
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.9',
    ],
)
