#!/bin/sh
base=$(basename $(pwd))
version=$(echo $base | sed 's/.*-\(.\+\)/\1/')
#release=$(lsb_release -cs)
release=$(dpkg-parsechangelog | grep ^Distribution: | sed 's/Distribution: //')
dch -v ${version}-1~getdeb1 -D ${release} New upstream version
