#!/usr/bin/env python

import os

from setuptools import setup, find_packages

requires = [
  'PrettyTable',
]

setup(name='denull_ops_tfstats',
      version='1.0.0',
      description='Gathers statistics from Terraform state files',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points={
        'console_scripts': [
            'tfstats = denull_ops_tfstats.main:main',
        ],
      },
)
