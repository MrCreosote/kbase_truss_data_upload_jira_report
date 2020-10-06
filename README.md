This repo contains code for producing data for a sprint report from a JIRA instance. It's
specifically designed for use with the Truss-KBase data upload project.

It's also a bit Q&D and probably fragile to API changes.

# Instructions

1. [Create a JIRA API token](https://confluence.atlassian.com/cloud/api-tokens-938839638.html).

# Resources

* [JIRA Cloud API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
* [Jira Agile API](https://docs.atlassian.com/jira-software/REST/7.0.4/)

# Potential improvements:

* [Use OAuth2 rather than an API token](https://developer.atlassian.com/cloud/jira/platform/security-for-other-integrations/)
* Add tests. Since this is just a JIRA summarization tool for management reporting, if it fails
  it's not critical, so time hasn't been spent here yet.
* Add code comments for functions. See above.
* Better error presentation. Currently just dumps out the entire response body from JIRA.
  See above.
