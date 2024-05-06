import unittest
from unittest.mock import MagicMock, patch

from Wrappers.BaseWrapper.base_wrapper import Wrapper
from Wrappers.BaseWrapper.base_wrapper_utils import SportKey


class TestBaseWrapper(unittest.TestCase):
    @patch('Wrappers.BaseWrapper.base_wrapper_utils.BaseWrapperUtils.init_client')
    @patch('Wrappers.BaseWrapper.base_wrapper_utils.BaseWrapperUtils.exchange_declare')
    def setUp(self, mock_init_client, mock_exchange_declare):
        # Mocking the BaseWrapperUtils class
        mock_init_client.return_value = MagicMock()
        mock_exchange_declare.return_value = MagicMock()
        self.wrapper = Wrapper("exchange", SportKey.FOOTBALL)

    @patch('Wrappers.BaseWrapper.base_wrapper_utils.BaseWrapperUtils.call_api')
    def test_collect_data(self, mock_call_api):
        test_url = 'url'

        mock_call_api.return_value = 'collected_data'
        result = self.wrapper.collect_data(test_url)

        # Assert that collect_data method returns collected_data
        self.assertEqual(result, 'collected_data')

    @patch('Wrappers.BaseWrapper.base_wrapper_utils.BaseWrapperUtils.publish_to')
    def test_publish_data(self, mock_publish_to):
        test_data = 'data'

        mock_publish_to.return_value = 'response'
        result = self.wrapper.publish_data(test_data)

        # Assert that publish_data method returns response
        self.assertEqual(result, 'response')


if __name__ == "__main__":
    unittest.main()
