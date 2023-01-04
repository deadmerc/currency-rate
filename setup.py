from setuptools import setup, find_packages

VERSION = '0.1.1'
long_description_text = """Python library for easy currency conversion.
Features:
List of currency rates relatively base currency
List of currencies
Get history currency rate
Convert one currency to another with specific amount
Currency symbols
Currency description
"""

setup(
    name='currency_rate',
    version=VERSION,
    author='Maxim Milchakov',
    author_email='maxim.milchakov@ya.ru',
    url='https://github.com/deadmerc/currency_rate',
    description='Exchange rates and currency conversion',
    long_description=long_description_text,
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'requests',
        'simplejson',
        'incremental',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Internationalization',
    ],
)