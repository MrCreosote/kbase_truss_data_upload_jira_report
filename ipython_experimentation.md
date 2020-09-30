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
```

