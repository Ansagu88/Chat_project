import unittest
from unittest.mock import patch, Mock
from chat.views import ask_openai

class TestAskOpenai(unittest.TestCase):
    """
    This class tests the ask_openai function in the chat.views module.
    """
    @patch('chat.views.openai.ChatCompletion.create')
    def test_ask_openai(self, mock_create):
        """
        This method tests the ask_openai function by mocking the openai.ChatCompletion.create method.

        It asserts that the function calls openai.ChatCompletion.create with the correct parameters,
        and that it returns the expected response.
        """
        mock_response = Mock()
        mock_response.choices = [{'message': {'content': 'Hello, how can I help you?'}}]
        mock_create.return_value = mock_response

        message = 'Hi'
        response = ask_openai(message)

        mock_create.assert_called_once_with(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ]
        )
        self.assertEqual(response, 'Hello, how can I help you?')