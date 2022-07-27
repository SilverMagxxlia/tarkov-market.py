import re

from setuptools import setup

requirements = []

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = ''
with open('tarkov_market/__init__.py') as f:
    search = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)

    if search is not None:
        version = search.group(1)

    else:
        raise RuntimeError("Could not grab version string")

if not version:
    raise RuntimeError("version is not set")

readme = ''

with open('README.rst') as f:
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
    long_description_content_type="text/x-rst",
    version=version,
    packages=packages,
    author='Hostagen',
    license='MIT',
    python_requires='>=3.8.0',
)
