# Notes on experimenting with the JIRA cloud API

```
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


```

