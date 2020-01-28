#!/usr/bin/python -u

# This script checks, if 'development' branch has all changes from 'master' branch on Git
# 'master' can have some changes, which 'development' does not have in case of hot fixes on 'master'

# Usage: compare-branches.py <path_to_your_git_repository>
# This script can be executed in a jenkins job from command line

import os, sys
from subprocess import Popen, PIPE
from time import sleep

def git_log():
    GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date', 'message']
    GIT_LOG_FORMAT = ['%H', '%an', '%ae', '%ad', '%s']
    GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e'

    p = Popen('git log --format="%s"' % GIT_LOG_FORMAT, shell=True, stdout=PIPE)
    (log, _) = p.communicate()
    log = log.strip('\n\x1e').split("\x1e")
    log = [row.strip().split("\x1f") for row in log]
    log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]
    return log

def git_checkout(branch_name):
    Popen('git checkout "%s"' % branch_name, shell=True, stdout=PIPE)

def commits_are_same(commit_one, commit_two):
    same_email = commit_one['author_email'] == commit_two['author_email']
    same_date = commit_one['date'] == commit_two['date']
    same_message = commit_one['message'] == commit_two['message']
    return same_email and same_date and same_message

def development_has_changes_from_master():
    # we need to add sleeps in this method
    # to read data from git correctly
    print ('Switching to \'master\'...')
    git_checkout('master')
    print ('Reading git log...')
    sleep(2)
    git_log_master = git_log()
    print ('Switching to \'development\'...')
    sleep(2)
    git_checkout('development')
    print ('Reading git log...')
    sleep(2)
    git_log_development = git_log()

    commit_found_array = []

    for commit_master in git_log_master:
        # if all elements in the array are False, commit wasn't found
        commit_not_found = not True in commit_found_array

        if(commit_found_array and commit_not_found):
            print ("ERROR: \'master\' needs to be merged into \'development\'")
            return False

        for commit_development in git_log_development:
            commit_found = commits_are_same(commit_master, commit_development)
            commit_found_array.append(commit_found)

    return True

def fail_jenkins_job():
    print ('Failing job...')
    sys.exit(-1) # when script will exit with non-zero status, jenkins job should fail

def compare_branches_in_repository():
    if len(sys.argv) == 1:
        print ('ERROR: path to repository is not defined')
        return

    path_to_repository = sys.argv[1]
    os.chdir(path_to_repository)

    if development_has_changes_from_master():
        print ('SUCCESS: \'development\' has all changes from \'master\'')
    else:
        fail_jenkins_job()

compare_branches_in_repository()
