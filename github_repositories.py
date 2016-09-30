#!/usr/bin/env python

import sys

# This program is optimized for Python 3.5

'''search_for parameter can be the follow values:
issues_url, has_wiki, forks_url, mirror_url, subscription_url,
notifications_url, collaborators_url, updated_at, private, pulls_url,
issue_comment_url, labels_url, full_name, owner, statuses_url, id, keys_
url, description, tags_url, network_count, downloads_url, assignees_url,
contents_url, git_refs_url, open_issues_count, clone_url, watchers_count,
git_tags_url, milestones_url, languages_url, size, homepage, fork, commits_
url, issue_events_url, archive_url, comments_url, events_url, contributors_
url, html_url, forks, compare_url, open_issues, git_url, svn_url, merges_url,
has_issues, ssh_url, blobs_url, master_branch, git_commits_url, hooks_url,
has_downloads, watchers, name, language, url, created_at, pushed_at, forks_
count, default_branch, teams_url, trees_url, organization, branches_url,
subscribers_url, and stargazers_url.'''

#Repositories for a specific user
#https://api.github.com/users/<user_name>/repos

GITHUB_URL_REPOS = 'https://api.github.com/repos'
GITHUB_URL_USERS = 'https://api.github.com/users'

import argparse
import requests
import json

def search_repository(author, repo, search_for):
    url = "%s/%s/%s" %(GITHUB_URL_REPOS, author, repo)
    print("Searching Repository URL: %s" %url)
    result = requests.get(url)
    if(result.ok):
        repo_info = json.loads(result.text or result.content)
        print("Github repository info for: %s" %repo)
        result = "No result found!"
        keys = []
        for key,value in repo_info.iteritems():
            if search_for in key:
                result = value
                return result

def search_repositories(author, search_for):
    url = "%s/%s/repos" %(GITHUB_URL_USERS, author)
    print("Searching Repositories URL: %s" %url)
    result = requests.get(url)
    if(result.ok):
        repo_info = json.loads(result.text or result.content)
        print("Github repository info for: %s" %author)
        result = "No result found!"
        keys = []
        for value in repo_info:
            for key,value2 in value.items():#python 2-->iteritems()
                if str(search_for)in str(key):
                    result = value
                    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Github search')
    parser.add_argument('--author', action="store", dest="author",required=True)
    parser.add_argument('--repo', action="store", dest="repo",required=False)
    parser.add_argument('--search_for', action="store",dest="search_for", default='owner', required=False)
    given_args = parser.parse_args()
    if given_args.repo is not None:
        result = search_repository(given_args.author, given_args.repo,given_args.search_for)
    else:
        result = search_repositories(given_args.author,given_args.search_for)
    if isinstance(result, dict):
        print("Got result for '%s'..." %(given_args.search_for))
        for key,value in result.items(): #python 2-->iteritems()
            print("%s => %s" %(key,value))
    else:
        print("Got result for %s: %s" %(given_args.search_for,result))