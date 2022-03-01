from setuptools import find_packages, setup
setup(
    name='signaturelib',
    packages=find_packages(include=['signaturelib']),
    version='0.1.0',
    description='Base application for signature',
    author='Python-Group-UFPS',
    license='MIT',
    install_requires=['sqlalchemy' ,'pymysql','pymupdf'],
)