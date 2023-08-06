import sys
import setuptools


long_description = '''VTPass by kodedFM'''

setuptools.setup(
    name="vtpassapi",
    version="1.1",
    url="",
    
    description="VTPass by kodedFM",
    long_description=long_description,
    license='Apache License Version 2.0',
    
    packages=setuptools.find_packages(),
    platforms='any',
    package_dir={"vtpassapi": "vtpassapi"},
    install_requires=[
        'requests',
    ],
    extras_require={},
    package_data={},
    classifiers=[],
)