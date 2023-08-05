#!/usr/bin/env python3
#
# check-dco.py: validate all commits are signed off
#
# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: GPL-2.0-or-later

import argparse
import os
import os.path
import sys
import subprocess

parser = argparse.ArgumentParser("check-dco")
parser.add_argument(
    "repourl",
    help="upstream repo URL"
)
parser.add_argument(
    "refspec",
    help="upstream's default branch (or other refspec)"
)
args = parser.parse_args()


def get_branch_commits(repourl, refspec):
    subprocess.check_call(["git", "remote", "add", "check-dco", repourl])
    subprocess.check_call(["git", "fetch", "check-dco", refspec],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)

    ancestor = subprocess.check_output(
        ["git", "merge-base", f"check-dco/{args.refspec}", "HEAD"],
        universal_newlines=True)
    ancestor = ancestor.strip()

    subprocess.check_call(["git", "remote", "rm", "check-dco"])

    return (ancestor, "HEAD")


def get_mergereq_commits():
    return (os.environ["CI_MERGE_REQUEST_DIFF_BASE_SHA"],
            os.environ["CI_MERGE_REQUEST_SOURCE_BRANCH_SHA"])


if os.environ.get("CI_PIPELINE_SOURCE", "") == "merge_request_event":
    ancestor, head = get_mergereq_commits()
else:
    ancestor, head = get_branch_commits(args.repourl, args.refspec)

errors = False

print("\nChecking for 'Signed-off-by: NAME <EMAIL>' " +
      "on all commits since %s...\n" % ancestor)

log = subprocess.check_output(["git", "log", "--format=%H %s",
                               f"{ancestor}...{head}"],
                              universal_newlines=True)

if log == "":
    commits = []
else:
    commits = [[c[0:40], c[41:]] for c in log.strip().split("\n")]

for sha, subject in commits:

    msg = subprocess.check_output(["git", "show", "-s", sha],
                                  universal_newlines=True)
    lines = msg.strip().split("\n")

    print("🔍 %s %s" % (sha, subject))
    sob = False
    for line in lines:
        if "Signed-off-by:" in line:
            sob = True
            if "localhost" in line:
                print("    ❌ FAIL: bad email in %s" % line)
                errors = True

    if not sob:
        print("    ❌ FAIL missing Signed-off-by tag")
        errors = True

if errors:
    print("""

❌ ERROR: One or more commits are missing a valid Signed-off-By tag.


This project requires all contributors to assert that their contributions
are provided in compliance with the terms of the Developer's Certificate
of Origin 1.1 (DCO):

  https://developercertificate.org/

To indicate acceptance of the DCO every commit must have a tag

  Signed-off-by: REAL NAME <EMAIL>

This can be achieved by passing the "-s" flag to the "git commit" command.

To bulk update all commits on current branch "git rebase" can be used:

  git rebase -i master -x 'git commit --amend --no-edit -s'

""")

    sys.exit(1)

sys.exit(0)
