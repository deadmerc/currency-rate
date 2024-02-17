from incremental import Version

__version__ = Version('CurrencyRate', 0, 1, 2)

from .converter import Converter

__all__ = '__version__', 'Converter'
