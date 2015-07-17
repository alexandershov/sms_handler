from setuptools import find_packages, setup

setup(
    name='sms_handler',
    version='0.1.0',
    install_requires=['django', 'requests'],
    packages=find_packages(),
)
