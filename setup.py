from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='autoupdate',
    version='2023.2',
    install_requires=requirements,
)