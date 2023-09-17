from setuptools import setup, find_packages

setup(
    name='firemangrid',
    version='0.1',
    author='Wenchang Gao',
    author_email='wenchang.gao@tufts.edu',
    packages=find_packages(),
    install_requires=[
        'gymnasium',
        'numpy',
        'pygame'
    ],
)
