#!/usr/bin/env python3

from setuptools import setup

setup(
    name='tscounters-py-nb',
    version='0.0.4',
    description='Time-series counters',
    author='Songyan Hou',
    author_email='songyan.hou@newsbreak.com',
    packages=['tscounters'],
    url="https://github.com/ParticleMedia/tscounters-py",
    keywords="opentsdb, metrics, counters",
    install_requires=[
        "requests",
        "prometheus_client",
    ]
)
