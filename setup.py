"""Скрипт Setup.py для проекта по упаковке."""

from setuptools import setup, find_packages

from PyQtUIkit.core._version import VERSION


def readme():
    with open('readme.md', 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='PyQtUIkit',
        author='SergeiKrivko',
        url='https://github.com/SergeiKrivko',
        long_description=readme(),
        version=VERSION,
        package_dir={'PyQtUIkit': 'PyQtUIkit'},
        packages=find_packages(include=['PyQtUIkit*']),
        description='A PyQtUIkit package.',
        install_requires=['PyQt6', 'lxml', 'beautifulsoup4'],
        python_requires='>=3.11'
    )
