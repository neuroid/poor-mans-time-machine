from setuptools import find_packages
from setuptools import setup


setup(name='poor-mans-time-machine',
      version='1.0.0',
      description='A simple tool for performing local incremental backups',
      author='Anonymous Coward',
      packages=find_packages(),
      install_requires=[
          'docopt',
      ],
      entry_points={
          'console_scripts': [
              'poor-mans-time-machine = poor_mans_time_machine.scripts.poor_mans_time_machine:main'
          ]
      })
