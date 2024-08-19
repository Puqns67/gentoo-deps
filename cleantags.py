#!/usr/bin/python

import json
import subprocess

print("=> Update local repository")
subprocess.run(["git", "fetch", "--tags", "--prune", "--prune-tags"])

print("=> Get github releases using github cli")
gh = subprocess.run(["gh", "release", "list", "--json", "tagName"], capture_output=True)
gh_releases = [v['tagName'] for v in json.loads(gh.stdout)]

print("=> Get tags using git from local repository")
git = subprocess.run(["git", "tag", "--list"], capture_output=True)
git_tags = [v.decode("utf-8") for v in git.stdout.split(b"\n") if v != b""]

print("=> Calculate what needs to be cleaned from repository")
git_tags_will_remove = []
for v in git_tags:
    if v not in gh_releases:
        git_tags_will_remove.append(v)

if len(git_tags_will_remove) == 0:
    print("=> No needed to clean, exited.")
    exit()

print("=> Clean tags of remote repository")
subprocess.run(["git", "push", "origin", "--delete"] + git_tags_will_remove)

print("=> Update local repository again")
subprocess.run(["git", "fetch", "--tags", "--prune", "--prune-tags"])
