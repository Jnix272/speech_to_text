import pytest
import requests
from unittest.mock import patch, MagicMock
from speech_to_text import make_request

def test_make_request_non_200_status():
    with patch('speech_to_text.requests.post') as mock_post:
        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        # Mock raise_for_status to do nothing
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = make_request("test prompt")

        # It should hit the else block and return a tuple: (status_code, text)
        assert result == (400, "Bad Request")

def test_make_request_200_status():
    with patch('speech_to_text.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Mistral API response returns a json with a 'response' string
        mock_response.text = '{"response": "Hello123world"}'
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = make_request("test prompt")

        # It should process the response, extract 'response', and remove digits
        assert result == "Helloworld"

def test_make_request_request_exception():
    with patch('speech_to_text.requests.post') as mock_post:
        # Mock requests.post to raise a RequestException
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        result = make_request("test prompt")

        assert result == "Error sending request: Connection error"
