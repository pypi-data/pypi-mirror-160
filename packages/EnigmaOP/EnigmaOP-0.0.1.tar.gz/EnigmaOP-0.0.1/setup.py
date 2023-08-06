from asyncore import read
from setuptools import setup, find_packages

classifires = [ 
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]
setup(
    name='EnigmaOP',
    version='0.0.1',
    description='Trail encryption methodology',
    long_description='Long description',
    url='',
    author='Ninad Hegde',
    author_email='ninadhegde@gmail.com',
    license='MIT',
    classifiers=classifires,
    keywords='EnigmaOP',
    packages=find_packages(),
    install_reuires=['']
)