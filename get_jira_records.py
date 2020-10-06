#!/usr/bin/env python3

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

MAX_RESULTS = 10


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


# *** side effect *** adds board ID to config
def get_jira_board(cfg):
    headers = get_auth_headers_from_config(cfg)

    not_complete = True
    boards = {}
    start_at = 0
    while not_complete:
        resp = requests.get(
            JIRA_URL + JIRA_BOARDS,
            params={QUERY_MAX_RESULTS: MAX_RESULTS, QUERY_START_AT: start_at},
            headers=headers)
        if not resp.ok:
            raise ValueError('Failed to get JIRA boards:\n' + resp.text)
        j = resp.json()
        not_complete = not j['isLast']
        start_at = start_at + MAX_RESULTS

        for board in j['values']:
            boards[board['name']] = board['id']
    sorted_boards = [(b, boards[b]) for b in sorted(boards)]
    
    print(f'Please choose a JIRA board:')
    for i, (board, _) in enumerate(sorted_boards):
        print(f'{i + 1}\t{board}')
    # could do a loop here, but assume the ppl using this are relatively intelligent
    board_num = input('Enter board number: ').strip()
    try:
        board_num = int(board_num)
    except ValueError:
        raise ValueError(f'Please enter an integer between 1-{len(sorted_boards)}')
    if board_num < 1 or board_num > len(sorted_boards):
        raise ValueError(f'Please enter an integer between 1-{len(sorted_boards)}')
    cfg.add_section(SEC_JIRA)
    cfg.set(SEC_JIRA, '# The ID of the JIRA agile board.', None)
    cfg[SEC_JIRA][CFG_BOARD] = str(sorted_boards[board_num - 1][1])


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
    headers = get_auth_headers_from_config(cfg)

    # similar to getting sprints above, maybe make a generic method
    not_complete = True
    sprints = {}
    start_at = 0
    while not_complete:
        resp = requests.get(
            f'{JIRA_URL}{JIRA_BOARDS}{board_id}{JIRA_SPRINT_SUFFIX}',
            params={QUERY_MAX_RESULTS: MAX_RESULTS, QUERY_START_AT: start_at},
            headers=headers)
        if not resp.ok:
            raise ValueError('Failed to get JIRA sprints:\n' + resp.text)
        j = resp.json()
        not_complete = not j['isLast']
        start_at = start_at + MAX_RESULTS

        for sprint in j['values']:
            sprints[sprint['name']] = sprint['id']
    sorted_sprints = [(b, sprints[b]) for b in sorted(sprints)]

    print(f'Please choose a sprint:')
    for i, (sprint, _) in enumerate(sorted_sprints):
        print(f'{i + 1}\t{sprint}')
    # could do a loop here, but assume the ppl using this are relatively intelligent
    sprint_num = input('Enter sprint number: ').strip()
    try:
        sprint_num = int(sprint_num)
    except ValueError:
        raise ValueError(f'Please enter an integer between 1-{len(sorted_sprints)}')
    if sprint_num < 1 or sprint_num > len(sorted_sprints):
        raise ValueError(f'Please enter an integer between 1-{len(sorted_sprints)}')
    return sorted_sprints[sprint_num - 1][1]


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
