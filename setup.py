from setuptools import find_packages, setup
setup(
    name='signature-lib',
    packages=find_packages(),
    version='1.1.2',
    description='Base application for signature',
    author='Python-Group-UFPS',
    license='MIT',
    install_requires=['requests'],
)