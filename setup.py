from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sqlalchemy-nest',
    version='1.0.0',
    description='easy create nested models for sqlalchemy',
    url='https://github.com/satorudev976/sqlalchemy-nest.git',
    packages=find_packages(),
    install_requires=["sqlalchemy>=0.7"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='satoru',
    license='MIT',
    python_requires='>=3.9',
    extras_require={
        "test": ["pytest", "pytest-cov"]
    }
)