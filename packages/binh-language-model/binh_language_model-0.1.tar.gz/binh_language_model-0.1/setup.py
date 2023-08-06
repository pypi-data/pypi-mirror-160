from setuptools import setup, find_packages
import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='binh_language_model',
    version='0.1',
    license='MIT',
    author="Nguyen Quoc Binh",
    author_email='binhquoc999@gmail.com',
    package_dir={'': 'src'},
    url='https://github.com/nqbinh17/language_model',
    keywords='language_model',
    packages=setuptools.find_packages(),
    install_requires=required
)