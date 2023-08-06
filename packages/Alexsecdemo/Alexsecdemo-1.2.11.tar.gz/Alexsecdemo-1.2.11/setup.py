from setuptools import setup
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
        name='Alexsecdemo', #package name
        version='1.2.11',
        description='A sample Python project, do not download it!',
        author='Alex',
        license='MIT',
        zip_safe=False,
        packages=['mymod1','mymod2','zzzsecdemo'],
        cmdclass={'install': CustomInstall},
        author_email='zhuzhuzhuzai@gmail.com'
)
