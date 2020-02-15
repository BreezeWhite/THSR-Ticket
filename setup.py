from setuptools import setup, find_packages

with open("requirements.txt", "r") as in_file:
    requirements = in_file.readlines()

setup(
    name='thsr_ticket',
    version='0.1',
    description='An automatic booking program for Taiwan High Speed Railway(THSR).',
    author='breezewhite',
    author_email='freedombluewater@gmail.com',
    packages=find_packages(),
    install_requires=requirements
)
