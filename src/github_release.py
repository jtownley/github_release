#!/usr/bin/env python

import requests
import os
import glob
import json
import argparse


class GitHubGateway(object):
    def __init__(self, username, token):
        self.token = token
        self.username = username
        self.session = requests.Session()
        self.session.auth = (self.username, self.token)
        self.headers = {
            "Content-Type": 'application/json',
            "Accepts": 'application/vnd.github.v3+json',
            'Authorization': 'token {}'.format(self.token),
        }
        print('Session created for user: {} with token starting with: {}'.format(self.username, self.token[:2]))

    def post_json_data(self, url, data):
        print('Posting to: "{}"'.format(url))
        print('Data: "{}"'.format(data))
        return self.session.post(url, data=data, headers=self.headers)

    def post_file(self, url, file_handle, params):
        return self.session.post(url, data=file_handle, params=params, headers=self.headers)


class GitHubRelease(object):
    def __init__(self, api=None, description_template=None, draft=False, files=[], name_template=None, owner=None, repo=None, tag=None, token=None, username=None):
        self._token_value = self._get_token_value(token)
        self.api_base_url = api
        self.draft = draft
        self.owner = owner
        self.repo = repo
        self.tag = tag
        self.username = username

        self._gateway = GitHubGateway(self.username, self._token_value)
        self.files = self._get_file_list(files)

        self.name = name_template.format(**self._key_dict)
        self.description = description_template.format(**self._key_dict)

    @property
    def _key_dict(self):
        return dict([(key, value) for (key, value) in self.__dict__.items() if key[0] != '_'])

    def _get_file_list(self, files):
        file_list = []
        for a_file in files:
            expanded_files = glob.glob(a_file)
            if len(expanded_files) == 0:
                raise Exception('No file(s) found matching "{}"'.format(a_file))
            file_list += expanded_files
        return file_list

    def _get_token_value(self, token):
        if not os.path.isfile(token):
            raise Exception('Could not find token file')
        with open(token, 'r') as token_file:
            token_value = token_file.read().strip()
        return token_value

    def _get_release_data(self):
        payload = {
            "tag_name": self.tag,
            "target_commitish": "master",
            "name": self.name,
            "body": self.description,
            "draft": self.draft,
            "prerelease": False
        }
        return json.dumps(payload, sort_keys=True, indent=4, separators=(',', ': '))

    def _publish_release(self):
        release_url = '{base}/repos/{owner}/{repo}/releases'.format(base=self.api_base_url, **self._key_dict)
        release_payload = self._get_release_data()
        result = self._gateway.post_json_data(release_url, release_payload)
        response_content = result.content
        if result.status_code != 201:
            raise Exception('Failed to create release: Got response code: {}  error: {}'.format(result.status_code, response_content))
        response_json = json.loads(response_content)
        if 'id' not in response_json:
            raise Exception('Failed to create release: Got response code: {}  response: {}'.format(result.status_code, response_content))
        return response_json

    def _publish_files(self, release_json):
        for afile in self.files:
            print ('Publishing Asset: "{}"'.format(afile))
            self._publish_file(release_json, afile)

    def _publish_file(self, release_json, afile):
        filename = os.path.basename(afile)
        url = release_json['upload_url'].split('{')[0]
        params = {'name': filename}
        with open(afile, 'r') as file_handle:
            result = self._gateway.post_file(url, file_handle, params)
        if result.status_code != 201:
            raise Exception('Failed to upload assets: Got response code: {}  error: {}'.format(result.status_code, result.content))

    def release(self,):
        for key, value in self._key_dict.items():
            print '"{}" = "{}"'.format(key, value)
        print "Beginning publish"
        release_json = self._publish_release()
        print "Release Created Successfully. Id: {}".format(release_json['id'])
        print "Begining file upload"
        self._publish_files(release_json)
        print "Files Publishing Complete"


if __name__ == "__main__":
    default_api = 'https://api.github.com'
    default_username = 'jtownley'
    default_token = 'token.txt'
    default_owner = 'PeachyPrinter'
    default_repo = 'peachyprintertools'
    default_name = 'Automated Release {tag}'
    default_description = ''

    supported_keys = ['username', 'owner', 'tokenfile', 'tag', 'api', 'url', 'repo', 'files']

    parser = argparse.ArgumentParser("Release to GitHub")
    parser.add_argument('-u', '--username',                          action='store',      required=True,                         help="Github username with push access")
    parser.add_argument('-o', '--owner',                             action='store',      required=True,                         help="GitHub repository owner")
    parser.add_argument('-t', '--token-file',                        action='store',      required=False, default=default_token, help="File containing the github token [{}]".format(default_token))
    parser.add_argument('-v', '--tag',                               action='store',      required=True,                         help="Tag version for release")
    parser.add_argument('-a', '--api',                               action='store',      required=False, default=default_api,   help='Base api url in the format "https://api.github.com" [{}]'.format(default_api))
    parser.add_argument('-r', '--repo',                              action='store',      required=True,                         help='Repository to update to')
    parser.add_argument('-f', '--files',                             action='append',     required=False,                        help='File to release (use this flag for each file(s)) wildcards in file ok.')
    parser.add_argument('-n', '--name',        dest='name_t',        action='store',      required=True,                         help='Name for the release accepts keys ({})'.format(', '.join(supported_keys)))
    parser.add_argument('-d', '--description', dest='description_t', action='store',      required=False, default='',            help='Description for release accepts keys ({}) []'.format(', '.join(supported_keys)))
    parser.add_argument('-k', '--draft',                             action='store_true', required=False, default=False,         help='Marks release as draft')
    args, unknown = parser.parse_known_args()

    api = args.api
    description_template = args.description_t
    draft = args.draft
    files = args.files
    name_template = args.name_t
    owner = args.owner
    repo = args.repo
    tag = args.tag
    token = args.token_file
    username = args.username

    GitHubRelease(
        api=api,
        description_template=description_template,
        draft=draft,
        files=files,
        name_template=name_template,
        owner=owner,
        repo=repo,
        tag=tag,
        token=token,
        username=username
    ).release()