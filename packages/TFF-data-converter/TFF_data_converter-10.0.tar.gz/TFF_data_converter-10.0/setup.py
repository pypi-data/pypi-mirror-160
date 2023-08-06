from setuptools import setup
import os
with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    install_requires=required,
    name='TFF_data_converter',
    version='10.0',
    packages=[''],
    url='',
    license='',
    author='Divya Reddy Polaka',
    author_email='polakadivya.reddy2019@vitstudent.ac.in',
    description='Tensorflow Federated data converter library'
)
