from setuptools import find_packages, setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name = 'twisel',
    packages=find_packages(include=['twisel']),
    version='0.1.11',
    description='Library for scraping twitter with selenium',
    author='rafiksept',
    license='MIT',
    install_requires = ['pytest','selenium','pandas'],
    test_suite = 'test',
    long_description=long_description,
    long_description_content_type='text/markdown'

)