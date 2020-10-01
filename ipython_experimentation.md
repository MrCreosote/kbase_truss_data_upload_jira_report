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

```

