from setuptools import setup
import re

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('tarkov_market/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''

with open('README.md') as f:
    readme = f.read()

packages = [
    'tarkov_market',
    'tarkov_market.types'
]

setup(
    name='tarkov-market.py',
    url='https://github.com/Hostagen/tarkov-market.py',
    description='async API wrapper for Tarkov Market written in Python.',
    long_description=readme,
    version=version,
    packages=packages,
    author='Hostagen',
    license='MIT',
    python_requires='>=3.8.0',
)
