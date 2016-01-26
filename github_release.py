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

    parser = argparse.ArgumentParser("Release to GitHub")
    parser.add_argument('-u', '--username',         dest='username',        action='store', required=True,  help="Enter the loglevel [DEBUG|INFO|WARNING|ERROR] default: WARNING")
    parser.add_argument('-o', '--owner',            dest='owner',           action='store', required=True,  help="Enter the loglevel [DEBUG|INFO|WARNING|ERROR] default: WARNING")
    parser.add_argument('-t', '--token-file',       dest='tokenfile',       action='store', required=False, default=default_token, help="Logs to console not file")
    parser.add_argument('-v', '--tag',              dest='tag',             action='store', required=True,  help="Enable Developer Testing Mode")
    parser.add_argument('-a', '--api',              dest='api',             action='store', required=False, help='Activate a module (use "list" to get a list of available modules).')
    parser.add_argument('-l', '--url',              dest='url',             action='store', required=False, default=default_url, help='override locale code')
    parser.add_argument('-r', '--repo',             dest='repo',            action='store', required=True,  help='override locale code')
    parser.add_argument('-f', '--files',            dest='files',           action='store', required=False, default='', help='override locale code')
    parser.add_argument('-n', '--name',             dest='name_t',          action='store', required=True,  help='override locale code')
    parser.add_argument('-d', '--description',      dest='description_t',   action='store', required=False, default=None, help='override locale code')
    parser.add_argument('-h', '--help',             dest='description',     action='store', required=False, default=None, help='override locale code')
    args, unknown = parser.parse_known_args()

    post_release_url = '{base}/repos/{owner}/{repo}/releases'.format(base=api_base, owner=owner, repo=repo)