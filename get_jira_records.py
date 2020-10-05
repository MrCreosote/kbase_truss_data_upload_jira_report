#!/usr/bin/env python3

import base64
import getpass
import os
import requests

from configparser import ConfigParser
from pathlib import Path

CONFIG_FILE = '.truss_kbase_jira_summary.cfg'
SEC_CREDS = 'Credentials'
CFG_USERNAME = 'username'
CFG_API_TOKEN = 'api_token'

JIRA_URL = 'https://kbase-jira.atlassian.net'
JIRA_API_TOKEN_URL = 'https://confluence.atlassian.com/cloud/api-tokens-938839638.html'
JIRA_MYSELF = '/rest/api/3/myself'


def get_auth_headers(username, token):
    return {'Authorization': 'Basic ' + base64.b64encode(
        f'{username}:{token}'.encode('UTF-8')).decode('UTF-8')}


def check_creds(username, token):
    resp = requests.get(JIRA_URL + JIRA_MYSELF, headers=get_auth_headers(username, token))
    if not resp.ok:
        raise ValueError('Authentication to JIRA failed:\n' + resp.text)


def load_config(cfgfile):
    cfg = ConfigParser()
    cfg.read(cfgfile)
    return cfg


def get_user_pass(cfg):
    username = input('Enter your JIRA user name (typically an email address): ')
    token = getpass.getpass(
        f'Enter your JIRA API token. You can get one from {JIRA_API_TOKEN_URL}: ')
    check_creds(username, token)
    
    cfg.add_section(SEC_CREDS)
    cfg.set(SEC_CREDS, '# The JIRA account username, often an email address.', None)
    cfg[SEC_CREDS][CFG_USERNAME] = username
    cfg.set(SEC_CREDS,
        '# An API token for the JIRA account, obtainable from ' + JIRA_API_TOKEN_URL, None)
    cfg[SEC_CREDS][CFG_API_TOKEN] = token


def get_config(cfgfile):
    cfg = ConfigParser(allow_no_value=True)
    get_user_pass(cfg)

    with open(cfgfile, 'w') as f:
        cfg.write(f)
    print(f'Wrote configuration to {cfgfile}. To make changes to the configuration you can ' +
        'edit that file manually or delete it to run this initialization routine again.')

    return cfg


def main():
    cfgfile = Path(os.path.expanduser('~')) / CONFIG_FILE
    if cfgfile.is_dir():
        raise ValueError(f'Configuration file {cfgfile} is a directory')
    if cfgfile.exists():
        print(f'Found configuration file {cfgfile}, loading')
        cfg = load_config(cfgfile)
    else:
        print(f'No configuration file found')
        cfg = get_config(cfgfile)


if __name__ == '__main__':
    main()
