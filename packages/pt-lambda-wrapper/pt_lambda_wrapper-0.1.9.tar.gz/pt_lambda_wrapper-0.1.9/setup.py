import re

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('README.md', encoding='utf-8') as fp:
    long_description = fp.read()

with open('requirements.txt', encoding='utf-8') as fp:
    install_requires = fp.read()

PACKAGE_NAME = 'pt_lambda_wrapper'
SOURCE_DIRECTORY = 'src'
SOURCE_PACKAGE_REGEX = re.compile(rf'^{SOURCE_DIRECTORY}')

source_packages = find_packages(include=[SOURCE_DIRECTORY, f'{SOURCE_DIRECTORY}.*'])
projects_packages = [SOURCE_PACKAGE_REGEX.sub(PACKAGE_NAME, name) for name in source_packages]

setup(name=PACKAGE_NAME,
      version='0.1.9',
      description='trigger wrapper for aws lambda application',
      author='JimmyMo',
      author_email='jocund_mo@aliyun.com',
      install_requires=install_requires,
      package_dir={PACKAGE_NAME: 'src'},
      packages=projects_packages,
      data_files=[('requirements.txt', ['requirements.txt'])],
      license="Apache License 2.0"
      )
