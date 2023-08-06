from setuptools import setup, find_packages
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        print('run custominstall successfully!')


setup(
        name='Bfixsecdemo', #package name
        version='1.0.0',
        description='A sample Python project, do not download it!',
        author='Bfix',
        license='MIT',
        # zip_safe=False,
        packages=find_packages(),
        py_modules=['Alexsecdemoraw'],
        cmdclass={'install': CustomInstall},
        author_email='zhuzhuzhuzai@gmail.com'
)
