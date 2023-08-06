from setuptools import setup, find_namespace_packages, find_packages

setup(
    name="mypackagesocool22072022",
    version="1.1",
    description='this package really cool',
    packages=find_namespace_packages(include=['russkikorablidinahui*']) + find_packages()
)