from setuptools import setup, find_packages

setup(
    name="unarea_core",
    version="2.0-dev",
    author="Alex",
    author_email="some@email.com",
    description="CORE",
    long_description="LONG",
    license="TBD",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'zc.buildout',
        'setuptools',
    ]
    # entry_points={
    #     'console_scripts': [
    #         'runserver = unarea_core.run:run']
    # }
)
