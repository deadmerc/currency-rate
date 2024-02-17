from setuptools import setup, find_packages

import currency_rate

with open('README.rst') as f:
    long_description_text = f.read()

setup(
    name='currency_rate',
    version=currency_rate.__version__.public(),
    author='Maxim Milchakov',
    author_email='maxim.milchakov@ya.ru',
    url='https://github.com/deadmerc/currency-rate',
    description='Exchange rates and currency conversion',
    long_description=long_description_text,
    long_description_content_type='text/x-rst',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'requests',
        'simplejson',
        'incremental',
        'pydantic',
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
