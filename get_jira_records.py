#!/usr/bin/env python3

# Passing the config around all over the place is pretty gross, esp considering that different
# functions expect different parts of the config to be present.
# If this ever becomes a tool that more than a few people use, that whole strategy should
# be rethought as it's not very maintainable.

import base64
import getpass
import os
import requests

from configparser import ConfigParser
from pathlib import Path

CONFIG_FILE = '.truss_kbase_jira_summary.cfg'
SEC_CREDS = 'Credentials'
SEC_JIRA = 'JIRA settings'
CFG_USERNAME = 'username'
CFG_API_TOKEN = 'api_token'
CFG_BOARD = 'board_id'

JIRA_URL = 'https://kbase-jira.atlassian.net'
JIRA_API_TOKEN_URL = 'https://confluence.atlassian.com/cloud/api-tokens-938839638.html'
JIRA_MYSELF = '/rest/api/3/myself/'
JIRA_BOARDS = '/rest/agile/1.0/board/'
JIRA_SPRINT_SUFFIX = '/sprint'
QUERY_MAX_RESULTS = 'maxResults'
QUERY_START_AT = 'startAt'
RESULT_IS_LAST = 'isLast'
RESULT_VALUES = 'values'
RESULT_NAME = 'name'
RESULT_ID = 'id'

MAX_RESULTS = 10000


def get_auth_headers(username, token):
    return {'Authorization': 'Basic ' + base64.b64encode(
        f'{username}:{token}'.encode('UTF-8')).decode('UTF-8')}


def get_auth_headers_from_config(cfg):
    username = cfg[SEC_CREDS][CFG_USERNAME]
    token = cfg[SEC_CREDS][CFG_API_TOKEN]
    return get_auth_headers(username, token)


def check_creds(username, token):
    resp = requests.get(JIRA_URL + JIRA_MYSELF, headers=get_auth_headers(username, token))
    if not resp.ok:
        raise ValueError('Authentication to JIRA failed:\n' + resp.text)


def load_config(cfgfile):
    cfg = ConfigParser()
    cfg.read(cfgfile)
    # TODO check config is valid - no missing keys, creds work, board ID is an int
    return cfg


# *** side effect *** - adds username, token, & comments to config
def get_user_pass(cfg):
    username = input('Enter your JIRA user name (typically an email address): ').strip()
    token = getpass.getpass(
        f'Enter your JIRA API token. You can get one from {JIRA_API_TOKEN_URL}: ').strip()
    check_creds(username, token)
    
    cfg.add_section(SEC_CREDS)
    cfg.set(SEC_CREDS, '# The JIRA account username, often an email address.', None)
    cfg[SEC_CREDS][CFG_USERNAME] = username
    cfg.set(SEC_CREDS, '# An API token for the JIRA account, obtainable from ', None)
    cfg.set(SEC_CREDS, '# ' + JIRA_API_TOKEN_URL, None)
    cfg[SEC_CREDS][CFG_API_TOKEN] = token


def get_jira_selection(username, token, url, name):
    headers = get_auth_headers(username, token)

    not_complete = True
    items = {}
    start_at = 0
    while not_complete:
        resp = requests.get(
            url,
            params={QUERY_MAX_RESULTS: MAX_RESULTS, QUERY_START_AT: start_at},
            headers=headers)
        if not resp.ok:
            raise ValueError(f'Failed to get {name}s:\n{resp.text}')
        j = resp.json()
        not_complete = not j[RESULT_IS_LAST]
        start_at = start_at + MAX_RESULTS

        for item in j[RESULT_VALUES]:
            items[item[RESULT_NAME]] = item[RESULT_ID]
    sorted_items = [(b, items[b]) for b in sorted(items)]
    
    print(f'Please choose a {name}:')
    for i, (item, _) in enumerate(sorted_items):
        print(f'{i + 1}\t{item}')
    # could do a loop here, but assume the ppl using this are relatively intelligent
    item_num = input(f'Enter {name} number: ').strip()
    try:
        item_num = int(item_num)
    except ValueError:
        raise ValueError(f'Please enter an integer between 1-{len(sorted_items)}')
    if item_num < 1 or item_num > len(sorted_items):
        raise ValueError(f'Please enter an integer between 1-{len(sorted_items)}')
    return sorted_items[item_num - 1][1]
    

# *** side effect *** adds board ID to config
def get_jira_board(cfg):
    board_id = get_jira_selection(
        cfg[SEC_CREDS][CFG_USERNAME],
        cfg[SEC_CREDS][CFG_API_TOKEN],
        f'{JIRA_URL}{JIRA_BOARDS}',
        'JIRA board'
    )
    cfg.add_section(SEC_JIRA)
    cfg.set(SEC_JIRA, '# The ID of the JIRA agile board.', None)
    cfg[SEC_JIRA][CFG_BOARD] = str(board_id)


def get_config(cfgfile):
    cfg = ConfigParser(allow_no_value=True)
    get_user_pass(cfg)
    get_jira_board(cfg)

    with open(cfgfile, 'w') as f:
        cfg.write(f)
    print(f'Wrote configuration to {cfgfile}. To make changes to the configuration you can ' +
        'edit that file manually or delete it to run this initialization routine again.')

    return cfg


def get_sprint_id(cfg):
    board_id = int(cfg[SEC_JIRA][CFG_BOARD])

    return get_jira_selection(
        cfg[SEC_CREDS][CFG_USERNAME],
        cfg[SEC_CREDS][CFG_API_TOKEN],
        f'{JIRA_URL}{JIRA_BOARDS}{board_id}{JIRA_SPRINT_SUFFIX}',
        'sprint')


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

    sprint_id = get_sprint_id(cfg)
    print(sprint_id)


if __name__ == '__main__':
    main()
