import unittest
import sys
import os
from mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from github_release import GitHubRelease

@patch('github_release.GitHubGateway')
class TestGitHubRelease(unittest.TestCase):
    def setUp(self,):
        self.expected_token_value = 'expected_token_value'
        self.expected_username = 'expected_username'
        self.expected_api = 'expected_api'
        self.files = []
        with open('test_token.txt', 'w') as token:
            token.write(self.expected_token_value)
        print os.path.join(os.path.dirname(__file__), 'test_token.txt')
        self.kwargs = {
            'api': self.expected_api,
            'token': os.path.join(os.path.dirname(__file__), 'test_token.txt'),
            'username': self.expected_username,
            'files': [],
        }

    def test_when_token_file_is_missing_exception_is_raised(self, mock_GitHubGateway):
        self.kwargs['token'] = 'not/a/file.txt'

        with self.assertRaises(Exception) as context:
            GitHubRelease(**self.kwargs)

        self.assertEqual('Could not find token file', context.exception.message)


    def test_init_creates_expected_gateway(self, mock_GitHubGateway):
        GitHubRelease(**self.kwargs)

        mock_GitHubGateway.assert_called_with(self.expected_username, self.expected_token_value, self.expected_api)

    def test_init_raises_if_file_specified_and_missing(self, mock_GitHubGateway):
        self.kwargs['files'] = ['fish.bork']

        with self.assertRaises(Exception) as context:
            GitHubRelease(**self.kwargs)

        self.assertEqual('No file(s) found matching "fish.bork"', context.exception.message)

    def test_init_raises_if_wildcard_file_specified_and_missing(self, mock_GitHubGateway):
        self.kwargs['files'] = ['*.bork']

        with self.assertRaises(Exception) as context:
            GitHubRelease(**self.kwargs)

        self.assertEqual('No file(s) found matching "*.bork"', context.exception.message)

if __name__ == '__main__':
    unittest.main()
