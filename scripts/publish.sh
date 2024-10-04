#!/usr/bin/bash
git checkout main
git tag $1
git push origin $1
git push origin --tags
git checkout dev
