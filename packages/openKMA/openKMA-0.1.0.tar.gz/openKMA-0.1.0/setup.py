from setuptools import setup, find_packages

setup(
    name = 'openKMA',
    version = '0.1.0',    
    description = 'Not yet description',
    url = 'https://github.com/taeyoon32/openKMA',
    author = 'Taeyoon Eom',
    author_email = 'eom.taeyoon.kor@gmail.com',
    license = 'MIT',
    packages = find_packages('src',exclude=['openKMA']),
    install_requires = ['requests',
                        'xmltodict',
                        'pandas',
                        'numpy'
                        ]
)