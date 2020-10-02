# Notes on experimenting with the JIRA cloud API

```python
In [1]: with open('/home/crushingismybusiness/.jira_cloud_token_gaprice_lbl_gov'
   ...: ) as f: 
   ...:     token = f.read().strip() 
   ...:

In [3]: import requests

In [4]: user = 'gaprice@lbl.gov'

In [5]: import base64

In [9]: authhdr = base64.b64encode(f'{user}:{token}'.encode('UTF-8')).decode('UT
   ...: F-8')

In [13]: resp = requests.get('https://kbase-jira.atlassian.net/rest/api/3/issue/
    ...: DATAUP-214', headers={'Authorization': f'Basic {authhdr}'})

In [14]: resp.text
Out[14]: '{"expand":"renderedFields,names,schema,operations,editmeta,changelog,versionedRepresentations","id":"36245","self":"https://kbase-jira.atlassian.net/rest/api/3/issue/36245","key":"DATAUP-214",
*snip*

# DU project sprint 5 ID is 86 (see in the jql query param last # is 86)
# Ideally allow user to provide sprint name vs sprint ID, seems non-trivial which is annoying

In [23]: resp = requests.get('https://kbase-jira.atlassian.net/rest/api/3/search
    ...: ?maxResults=1000&jql=Sprint%20%3D%2086', headers={'Authorization': f'Ba
    ...: sic {authhdr}'})

# need to check if need to pull more issues

In [26]: j['maxResults']
Out[26]: 100

In [27]: j['total']
Out[27]: 21

In [35]: for issue in j['issues']:
    ...:     print(issue['key'])
    ...:
DATAUP-235
DATAUP-234
DATAUP-233
DATAUP-232
DATAUP-231
DATAUP-230
DATAUP-228
DATAUP-227
DATAUP-217
DATAUP-214
DATAUP-204
DATAUP-203
DATAUP-202
DATAUP-197
DATAUP-194
DATAUP-188
DATAUP-181
DATAUP-178
DATAUP-176
DATAUP-128
DATAUP-87

# story point fields:
# customfield_11164	Story points actual
# customfield_11127	Story point estimate

# need check and see if pull more records
In [57]: resp = requests.get('https://kbase-jira.atlassian.net/rest/api/3/issue/
    ...: DATAUP-194/changelog?maxResults=1000', headers={'Authorization': f'Basi
    ...: c {authhdr}'})
    ...:

In [58]: j = resp.json()

# j['total'] = 16

# use IDs rather than strings in actual code, ids are in the item map
In [59]: for change in j['values']:
    ...:     for item in change['items']:
    ...:         if item['field'] == 'status':
    ...:             print(f"{change['created']}\t{item['fromString']}\t{item['t
    ...: oString']}")
    ...:
2020-09-24T09:49:32.533-0700	To Do	In Progress
2020-09-24T13:07:32.385-0700	In Progress	On Hold/Blocked
2020-09-25T11:28:26.453-0700	On Hold/Blocked	In Progress
2020-09-28T09:32:55.325-0700	In Progress	On Hold/Blocked
2020-09-29T14:44:34.626-0700	On Hold/Blocked	Test/Feedback
2020-09-29T15:01:50.643-0700	Test/Feedback	In Progress
2020-09-30T16:03:01.492-0700	In Progress	Done

# sprint field ID is customfield_10400

#### Look up sprint ID ####

In [81]: resp = requests.get('https://kbase-jira.atlassian.net/rest/agile/1.0/bo
    ...: ard?maxResults=1000', headers={'Authorization': f'Basic {authhdr}'})

In [87]: for board in j['values']:
    ...:     print(board['name'])
    ...:
Sprints
PTV board
ITB board
Implementation Kanban
Review Proposals/Bugs
Product Team View (Deprecated- use Epic)
Product Descriptions
Product Description Scrum
SCT board
Epic (Current Product Team)
APS
TESTE2 board
DevOps Board
KBASEDATA2 board
Metrics
Devops Open Tickets

In [88]: j['values'][-3]
Out[88]:
{'id': 57,
 'self': 'https://kbase-jira.atlassian.net/rest/agile/1.0/board/57',
 'name': 'KBASEDATA2 board',
 'type': 'simple',
 'location': {'projectId': 11023,
  'displayName': 'Truss Data Upload (DATAUP)',
  'projectName': 'Truss Data Upload',
  'projectKey': 'DATAUP',
  'projectTypeKey': 'software',
  'avatarURI': '/secure/projectavatar?size=small&s=small&pid=11023&avatarId=12618',
  'name': 'Truss Data Upload (DATAUP)'}}

In [89]: resp = requests.get('https://kbase-jira.atlassian.net/rest/agile/1.0/bo
    ...: ard/57/sprint?maxResults=1000', headers={'Authorization': f'Basic {auth
    ...: hdr}'})


In [93]: for sprint in j['values']:
    ...:     print(f"{sprint['id']}\t{sprint['name']}")
    ...:
80	KBASEDAT Sprint 1
81	KBASEDAT Sprint 2
83	KBASEDAT Sprint 3
85	KBASEDAT Sprint 4
86	KBASEDAT Sprint 5

#### Getting custom field IDs ####

In [94]: In [23]: resp = requests.get('https://kbase-jira.atlassian.net/rest/api
    ...: /3/search?maxResults=1000&expand=names&jql=Sprint%20%3D%2086', headers=
    ...: {'Authorization': f'Basic {authhdr}'})

In [99]: j['names']
Out[99]:
{'statuscategorychangedate': 'Status Category Changed',
 'parent': 'Parent',
 'issuetype': 'Issue Type',
 'customfield_11160': 'Target start',
 'customfield_11161': 'Target end',
 'timespent': 'Time Spent',
 'customfield_11163': 'Reviewer',
 'customfield_11164': 'Story points actual',
 'project': 'Project',
*snip*

#### Getting story points ####
In [119]: resp = requests.get('https://kbase-jira.atlassian.net/rest/api/3/searc
     ...: h?maxResults=1000&jql=Sprint%20%3D%2085', headers={'Authorization': f'
     ...: Basic {authhdr}'})

In [120]: issues = resp.json()

In [121]: for issue in issues['issues']:
     ...:     fields = issue['fields']
     ...:     print(f"{fields.get('customfield_11127')}\t{fields.get('customfiel
     ...: d_11164')}")
     ...:
None	None
None	None
2.0	1.0
None	None
None	None
None	None
None	None
None	None
1.5	1.5
1.0	None
None	None
None	None
None	None
None	None
None	None
3.0	None
0.75	1.5
1.0	0.4
None	None
1.0	None
1.0	None
1.0	None
0.25	0.125
0.5	0.75
0.25	0.1
1.0	1.0
2.0	2.0
1.0	None
1.0	None
1.0	None
1.0	None
1.0	None
1.5	3.0
1.0	None
None	None
1.0	None
5.0	None
None	None
None	None

#### Getting changelog per issue ####

In [124]: changelog = {}

In [127]: for issue in issues['issues']:
     ...:     key = issue['key']
     ...:     resp = requests.get(f'https://kbase-jira.atlassian.net/rest/api/3/
     ...: issue/{key}/changelog?maxResults=1000', headers={'Authorization': f'Ba
     ...: sic {authhdr}'})
     ...:     changelog[key] = resp.json()

# manually check we're not missing any logs. Loop over this in actual
# implementation

In [135]: for c in changelog.values():
     ...:     print(c['isLast'])
     ...:
True
True
True
*snip*

# this logic is probably not the cleanest

In [136]: def get_proc_to_done(changelog):
     ...:     proc = '9999999999'
     ...:     done = '0000000000'
     ...:     for change in changelog['values']:
     ...:         for item in change['items']:
     ...:             if item['field'] == 'status':
     ...:                 # use IDs here, not strings
     ...:                 if item['toString'] == 'In Progress':
     ...:                     if change['created'] < proc:
     ...:                         proc = change['created']
     ...:                 if item['toString'] == 'Done':
     ...:                     if change['created'] > done:
     ...:                         done = change['created']
     ...:                 if item['toString'] != 'Done':
     ...:                     done = '0000000000'
     ...:     proc = proc if proc != '9999999999' else None
     ...:     done = done if done != '0000000000' else None
     ...:     return proc, done
     ...:

In [137]: for key in changelog:
     ...:     print(key, get_proc_to_done(changelog[key]))
     ...:
DATAUP-227 (None, None)
DATAUP-216 (None, None)
DATAUP-214 ('2020-09-28T10:17:22.913-0700', '2020-09-30T13:57:36.022-0700')
DATAUP-207 ('2020-09-23T13:20:00.260-0700', '2020-09-28T09:37:46.147-0700')

# summary

In [41]: for issue in issues['issues']:
    ...:     fields = issue['fields']
    ...:     expec = fields.get('customfield_11127') or ''
    ...:     actual = fields.get('customfield_11164') or ''
    ...:     proc, done = get_proc_to_done(changelog[issue['key']])
    ...:     proc = proc or ''
    ...:     done = done or ''
    ...:     if proc:
    ...:         proc = dateutil.parser.isoparse(proc)
    ...:         proc = f'{proc:%Y-%m-%d %H:%M:%S}'
    ...:     if done:
    ...:         done = dateutil.parser.isoparse(done)
    ...:         done = f'{done:%Y-%m-%d %H:%M:%S}'
    ...:     print(f"{issue['key']}\t{expec}\t{actual}\t{proc}\t{done}")
    ...:
    ...:
DATAUP-227
DATAUP-216
DATAUP-214	2.0	1.0	2020-09-28 10:17:22	2020-09-30 13:57:36
DATAUP-207			2020-09-23 13:20:00	2020-09-28 09:37:46

```

