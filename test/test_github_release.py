import unittest
import sys
import os
import json
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
        self.expected_name_template = 'expected_name_template'
        self.expected_owner = 'expected_owner'
        self.expected_description_template = 'expected_description_template'
        self.expected_tag = "Expected Tag"
        self.expected_repo = "expected_repo"
        self.expected_draft = False
        self.files = []
        with open('test_token.txt', 'w') as token:
            token.write(self.expected_token_value)
        self.kwargs = {
            'api': self.expected_api,
            'description_template': self.expected_description_template,
            'draft': self.expected_draft,
            'files': [],
            'name_template': self.expected_name_template,
            'owner': self.expected_owner,
            'repo': self.expected_repo,
            'tag': self.expected_tag,
            'token': os.path.join(os.getcwd(), 'test_token.txt'),
            'username': self.expected_username,

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

    def test_init_creates_name_with_keys(self, mock_GitHubGateway):
        self.kwargs['username'] = 'Booya'
        self.kwargs['owner'] = 'Chicken'
        self.kwargs['name_template'] = '{username} is {owner}'
        expected = 'Booya is Chicken'

        ghr = GitHubRelease(**self.kwargs)

        self.assertEqual(expected, ghr.name)

    def test_init_creates_description_with_keys(self, mock_GitHubGateway):
        self.kwargs['username'] = 'Fruit'
        self.kwargs['owner'] = 'Llamas'
        self.kwargs['description_template'] = '{username} {owner} are the bomb'
        expected = 'Fruit Llamas are the bomb'

        ghr = GitHubRelease(**self.kwargs)

        self.assertEqual(expected, ghr.description)

    def test_release_calls_post_json_data_with_correct_url_and_data_for_release(self, mock_GitHubGateway):
        self.kwargs['owner'] = 'Big'
        self.kwargs['repo'] = 'Canary'
        expected_url = '/repos/Big/Canary/releases'
        expected_data = json.dumps({
              "tag_name": self.kwargs['tag'],
              "target_commitish": "master",
              "name": self.kwargs['name_template'],
              "body": self.kwargs['description_template'],
              "draft": False,
              "prerelease": False
            }, sort_keys=True, indent=4, separators=(',', ': '))

        ghr = GitHubRelease(**self.kwargs)
        ghr.release()

        mock_GitHubGateway.return_value.post_json_data.assert_called_with(expected_url, expected_data)

    def test_release_calls_post_json_data_with_correct_url_and_data_for_release_when_draft(self, mock_GitHubGateway):
        self.kwargs['owner'] = 'Big'
        self.kwargs['repo'] = 'Canary'
        expected_url = '/repos/Big/Canary/releases'
        self.kwargs['draft'] = True
        expected_data = json.dumps({
              "tag_name": self.kwargs['tag'],
              "target_commitish": "master",
              "name": self.kwargs['name_template'],
              "body": self.kwargs['description_template'],
              "draft": True,
              "prerelease": False
            }, sort_keys=True, indent=4, separators=(',', ': '))

        ghr = GitHubRelease(**self.kwargs)
        ghr.release()

        mock_GitHubGateway.return_value.post_json_data.assert_called_with(expected_url, expected_data)

if __name__ == '__main__':
    unittest.main()
