#!/usr/bin/env python

import urllib2
import json
import argparse

api_base = 'https://api.github.com'
username = 'jtownley'
token = '9cada3e26863e50fbf22dd9124bd54f77e22fe27'
owner = 'PeachyPrinter'
repo = 'peachyprintertools'
post_release_url = '{base}/repos/{owner}/{repo}/releases'.format(base=api_base, owner=owner, repo=repo)


# password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
# password_mgr.add_password(None, api_base, username, token)
# handler = urllib2.HTTPBasicAuthHandler(password_mgr)
# opener = urllib2.build_opener(handler)

# result = opener.open(api_base +'/repos/{}/{}/releases'.format(owner, repo))
# release_data = json.loads(result.read())
# print json.dumps(release_data, sort_keys=True, indent=4, separators=(',', ': '))


class GitHubGateway(object):
    pass

class GitHubRelease(object):
    post_release_url = '{base}/repos/{owner}/{repo}/releases'.format(base=api_base, owner=owner, repo=repo)
    pass

if __name__ == "__main__":
    default_api = 'https://api.github.com'
    default_url = '{base}/repos/{owner}/{repo}/releases'
    default_username = 'jtownley'
    default_token = 'token.txt'
    default_owner = 'PeachyPrinter'
    default_repo = 'peachyprintertools'
    default_files = '*.zip *.tar.gz'
    default_name = 'Automated Release {tag}'
    default_description = ''

    supported_keys = ['username', 'owner', 'tokenfile', 'tag', 'api', 'url', 'repo', 'files']

    parser = argparse.ArgumentParser("Release to GitHub")
    parser.add_argument('-u', '--username',    dest='username',      action='store',      required=True,                         help="Github username with push access")
    parser.add_argument('-o', '--owner',       dest='owner',         action='store',      required=True,                         help="GitHub repository owner")
    parser.add_argument('-t', '--token-file',  dest='tokenfile',     action='store',      required=False, default=default_token, help="File containing the github token [{}]".format(default_token))
    parser.add_argument('-v', '--tag',         dest='tag',           action='store',      required=True,                         help="Tag version for release")
    parser.add_argument('-a', '--api',         dest='api',           action='store',      required=False, default=default_api,   help='Base api url in the format "https://api.github.com" [{}]'.format(default_api))
    parser.add_argument('-l', '--url',         dest='url',           action='store',      required=False, default=default_url,   help='Url of the releases post in the format "/url" accepts keys ({}) [{}]'.format(', '.join(supported_keys), default_url))
    parser.add_argument('-r', '--repo',        dest='repo',          action='store',      required=True,                         help='Repository to update to')
    parser.add_argument('-f', '--files',       dest='files',         action='store',      required=False, default=default_files, help='List of files to release wildcards in files ok. [{}]'.format(default_files))
    parser.add_argument('-n', '--name',        dest='name_t',        action='store',      required=True,                         help='Name for the release accepts keys ({})'.format(', '.join(supported_keys)))
    parser.add_argument('-d', '--description', dest='description_t', action='store',      required=False, default=None,          help='Description for release accepts keys (see --help) []')
    parser.add_argument('-k', '--draft',       dest='draft',         action='store-true', required=False, default=None,          help='Marks release as draft')
    parser.add_argument('-q', '--quiet',       dest='quiet',         action='store-true', required=False, default=None,          help='Only prints errors')
    args, unknown = parser.parse_known_args()

