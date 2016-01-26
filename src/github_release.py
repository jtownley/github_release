#!/usr/bin/env python

import urllib2
import os
import glob
import json
import argparse

# password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
# password_mgr.add_password(None, api_base, username, token)
# handler = urllib2.HTTPBasicAuthHandler(password_mgr)
# opener = urllib2.build_opener(handler)

# result = opener.open(api_base +'/repos/{}/{}/releases'.format(owner, repo))
# release_data = json.loads(result.read())
# print json.dumps(release_data, sort_keys=True, indent=4, separators=(',', ': '))


class GitHubGateway(object):
    def __init__(self, username, token, base_url):
        pass

    def post_json_data(self, url, data):
        pass

    def post_file(self, url, type, name, data):
        pass


class GitHubRelease(object):
    def __init__(self, api=None, description_template=None, draft=False, files=[], name_template=None, owner=None, repo=None, tag=None, token=None, username=None):
        self._token_value = self._get_token_value(token)
        self.api_base_url = api
        self.draft = draft
        self.owner = owner
        self.repo = repo
        self.tag = tag
        self.username = username

        self._gateway = GitHubGateway(self.username, self._token_value, self.api_base_url)
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

    def _get_token_value(self, token):
        if not os.path.isfile(token):
            raise Exception('Could not find token file')
        with open(token, 'r') as token_file:
            token_value = token_file.read()
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

    def release(self,):
        release_url = '/repos/{owner}/{repo}/releases'.format(**self._key_dict)
        release_payload = self._get_release_data()
        print ('Posting to {}\n payload: {}'.format(release_url, release_payload))
        result = self._gateway.post_json_data(release_url, release_payload)
        if result.getcode() != 201:
            raise Exception('Failed to create release: Got response code: {}  error: {}'.format(result.getcode(), result.read()))
        response_content = result.read()
        response_json = json.loads(response_content)
        if 'id' not in response_json:
            raise Exception('Failed to create release: Got response code: {}  response: {}'.format(result.getcode(), response_content))


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
    description_template = args.description
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

