"""Setup for vqproblem XBlock."""

import os
from setuptools import setup


def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='vqproblem-xblock',
    version='0.1',
    description='vqproblem XBlock',   # TODO: write a better description.
    packages=[
        'vqproblem',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'vqproblem = vqproblem:VideoQuizProblem',
        ]
    },
    package_data=package_data("vqproblem", "static"),
)