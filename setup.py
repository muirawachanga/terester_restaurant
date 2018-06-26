from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='terester_restaurant',
    version=version,
    description='App for managing Hotel Properties',
    author='Terester Company Limited',
    author_email='wachangasteve@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
