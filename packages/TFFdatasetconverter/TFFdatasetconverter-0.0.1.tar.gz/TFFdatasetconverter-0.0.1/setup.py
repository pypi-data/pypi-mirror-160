from setuptools import setup
import os
with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    install_requires=required,
    name='TFFdatasetconverter',
    version='0.0.1',
    packages=[''],
    url='',
    license='MIT',
    author='Divya Reddy Polaka',
    author_email='polakadivya.reddy2019@vitstudent.ac.in',
    description='Tensorflow Federated data converter library'
)
