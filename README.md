git-expand-filter
=================

Smudge/clean script and files for transparently expanding variables in files committed to git repositories.

Usage
-----

Execute the following lines to add the filter to your .git/config:
    $ git config filter.expand.smudge "expand.py smudge --local local.conf"
    $ git config filter.expand.clean "expand.py clean"
Then delete and checkout 'test.txt' to see the filter in action:
    $ cat test.txt
    line one
    stuff and $CommitInfo$junk
    line three
    other stuff and $More$ junk
    line five
    $ rm test.txt
    $ git checkout test.txt
    $ cat test.txt
    line one
    stuff and $CommitInfo: Tue Oct 15 22:43:27 2013 -0400 80c51898c28bc7ae54425a2cc84a08c97dce7f7f add note to README$junk
    line three
    other stuff and $More: Here's even more!$ junk
    line five

Notes
-----

The following command should output nothing (not even blank lines):
    cat clean.txt | expand.py smudge --local local.conf | expand.py clean | diff - clean.txt
