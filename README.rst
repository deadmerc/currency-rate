currency-rate
=============

Python library for easy convert currencies

Features:
--------
- List of currency rates relatively base currency
- List of currencies
- Get history currency rate
- Convert one currency to another with specific amount
- Currency symbols
- Currency description

Installation
--------------

- Install using python package

	.. code-block:: python

			pip install currency-rate

				Or directly cloning the repo:

			python setup.py install


Usage Examples:
------------------

	.. code-block:: python

			>>> from currency_rate.converter import Converter
			>>> converter = Converter()
			>>> converter.rate('USD', 'GEL')
			2.683433
			>>> converter.rate('EUR', 'USD', 50)
			52.880896
			>>> from datetime import date
			>>> converter.rate('EUR', 'USD', 50, date(2022, 4, 10))
			54.453328
			>>> converter.rate('EUR', 'UNK', 50)
			InvalidCurrencyException: UNK
			>>> converter.rate('EUR', 'UNK', 50, verify=False)
			None



