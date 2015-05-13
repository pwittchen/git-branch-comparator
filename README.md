# git-branch-comparator
Python script, which checks if *development* branch has all changes from *master* branch on Git repository

Description
-----------

When we are working in a Git Flow and critical bug occurs on production, sometimes there is a necessity to create so called *hot-fix*. We can create separate branch from *master* branch for this *hot-fix* and then merge it into *master* branch or we can commit a change on *master* branch. Second option is not recommended.
After that, we have to remember to merge *master* branch into a *development* branch to have our *hot-fix* in a development version as well and avoid merge conflicts in the future.

This Python script checks, if all changes made on *master* branch were also merged into *development* branch to keep those two branches consistent. We can add it as a job into Jenkins CI server and monitor branches consistency. In addition, release jobs can be dependend on that job and we can avoid merge conflicts or project unstability before release.

Usage
-----

`$ compare-branches.py <path_to_your_git_repository>`

Integration with Jenkins
------------------------

This script can be executed as a command line script in a Jenkins CI job.
When, changes from *master* won't be merged into *development*, job will fail. In opposite case, job should finish with a success.
