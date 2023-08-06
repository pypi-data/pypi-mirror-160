'''
Author: Vincent Young
Date: 2022-07-24 04:27:43
LastEditors: Vincent Young
LastEditTime: 2022-07-24 04:30:31
FilePath: /GenchAPI/setup.py
Telegram: https://t.me/missuo

Copyright © 2022 by Vincent, All Rights Reserved. 
'''
from setuptools import setup, find_packages


setup(
    name="GenchAPI",
    author="missuo",
    version="0.0.1",
    license='MIT',
    author_email="i@yyt.moe",
    description="GenchEDU SDK",
    url='https://github.com/GenchEDU/GenchAPI',
    packages=find_packages(),
    include_package_data=False,
    platforms='any',
    zip_safe=False,

    install_requires=[
        'requests',
        'bs4',
        'lxml',
        'bs4'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

)