import os
from setuptools import setup, find_packages

__version__ = '0.0.1'
_path = os.path.abspath(os.path.dirname(__file__))
_README = """LONG README HERE"""
_CHANGES = """RELEASE CHANGELOG HERE"""

setup(
    name="unarea_core",
    version=__version__,
    description="CORE",
    long_description=_README + '\n \n' + _CHANGES,
    author="alex",
    license="OPEN",
    packages=find_packages(),
    author_email="info@drs.systems",
    install_requires=[
        'zc.buildout',
        'setuptools',
        'tornado==4.2'
    ],
    entry_points={
        'console_scripts': [
            'cli/server/main_server = unarea_core.application:main'
        ]
    }
)
