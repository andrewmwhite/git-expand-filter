git-expand-filter
=================

Smudge/clean script and files for transparently expanding variables in files committed to git repositories.

Notes
-----

The following command should output nothing (not even blank lines):
    cat clean.txt | expand.py smudge --local local.conf | expand.py clean | diff - clean.txt
