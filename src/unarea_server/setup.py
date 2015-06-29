import os
from setuptools import setup, find_packages

__name__ = "unarea_server"
__version__ = '0.0.1'
_path = os.path.abspath(os.path.dirname(__file__))
_README = """LONG README HERE"""
_CHANGES = """RELEASE CHANGELOG HERE"""

setup(
    name="unarea_server",
    version=__version__,
    description="unarea_server",
    long_description=_README + '\n \n' + _CHANGES,
    author="alex",
    license="OPEN",
    packages=find_packages(),
    author_email="info@drs.systems",
    requires=['tornado'],
    entry_points={
        'console_scripts': [
            'runserver = unarea_server.manager.server:runserver'
        ]
    }
)
# setup(
#     name=__name__,
#     version='0.0.1',
#     author="drs",
#     author_email="info@drs.systems",
#     description="Dispareng framework",
#     long_description=_README + '\n \n' + _CHANGES,
#     license="DRS MAIN",
#     packages=find_packages(),
#     include_package_data=True,
#     zip_safe=False,
# )
