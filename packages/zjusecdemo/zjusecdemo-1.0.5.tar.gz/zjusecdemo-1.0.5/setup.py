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
        name='zjusecdemo', #package name
        version='1.0.5',
        description='A sample Python project, do not download it!',
        author='Alex',
        license='MIT',
        packages=['mymod1','mymod2'],
        py_modules=['Alexsecdemoraw'],
        cmdclass={'install': CustomInstall},
        author_email='zhuzhuzhuzai@gmail.com',
        # install_requires=[
        # "Bfixsecdemo==1.0.1",
        # ],
)
