import unittest
from unittest.mock import patch, Mock

from currency_rate.converter import Converter


class TestConverter(unittest.TestCase):
    @patch('currency_rate.converter.RequestSession', autospec=True)
    def test_symbols_list(self, MockRequestSession):
        mock_session = Mock()
        mock_session.get.return_value.status_code = 200
        mock_session.get.return_value.json.return_value = {'data': [{'symbol': 'USD', 'title': 'US Dollar'}]}
        MockRequestSession.return_value.__enter__.return_value = mock_session

        converter = Converter()
        symbols = converter.symbols.list

        self.assertEqual(len(symbols), 1)
        self.assertEqual(symbols[0].symbol, 'USD')


if __name__ == '__main__':
    unittest.main()
