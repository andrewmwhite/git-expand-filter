#!/usr/bin/env python

from __future__ import print_function

import re
import sys
import argparse
import subprocess

GITLOGCMD="""git log --pretty=format:"%ad %H %s" -1"""

def smudge(args):
  replacements = dict({
    'CommitInfo': subprocess.check_output(GITLOGCMD, shell=True),
  })

  if args.local is not None:
    try:
      f = open(args.local)
    except IOError as e:
      print(str(e), file=sys.stderr)
    else:
      for line in f:
        (key, value) = line.strip().split(': ', 1)
        replacements[key] = value
      f.close()

  #print("smudging...", file=sys.stderr)
  #print("replacements: {!s}".format(replacements), file=sys.stderr)

  def repl(m):
    return """${:s}: {!s}$""".format(m.group(1), replacements[m.group(1)])

  pattern = """\$({:s})\$""".format('|'.join(replacements.keys()))

  #print("pattern: {:s}".format(pattern), file=sys.stderr)
  print(re.sub(pattern, repl, sys.stdin.read()), end='')

def clean(args):
  #print("cleaning...", file=sys.stderr)
  pattern     = """\$([^:]+): [^\$]*\$"""
  replacement = """$\g<1>$"""
  print(re.sub(pattern, replacement, sys.stdin.read()), end='')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(\
      description="""Smudge and clean scripts for git.""")
  subparsers = parser.add_subparsers()

  parser_smudge = subparsers.add_parser('smudge')
  parser_smudge.add_argument("--local", dest="local", \
    type=str, default=None)
  parser_smudge.set_defaults(func=smudge)

  parser_clean  = subparsers.add_parser('clean')
  parser_clean.set_defaults(func=clean)

  args = parser.parse_args()
  args.func(args)
