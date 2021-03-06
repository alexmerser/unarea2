from setuptools import setup, find_packages

setup(
    name="unarea_core",
    version="2.0.dev0",
    author="Alex",
    author_email="some@email.com",
    description="CORE",
    long_description="LONG",
    license="TBD",
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['zc.buildout', 'setuptools'],
    entry_points={
        'console_scripts': [
            'run_server = unarea_core.run:run_local'
        ]
    }
)
