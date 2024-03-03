"""Скрипт Setup.py для проекта по упаковке."""


from setuptools import setup, find_packages

from PyQtUIkit.core._version import VERSION

if __name__ == '__main__':
    setup(
        name='PyQtUIkit',
        version=VERSION,
        package_dir={'PyQtUIkit': 'PyQtUIkit'},
        packages=find_packages(include=['PyQtUIkit*']),
        description='A PyQtUIkit package.',
        install_requires=['PyQt6', 'bs4']
    )
