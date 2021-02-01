#!/bin/bash

set -eu

topdir=$(dirname "$0"| xargs readlink -f | xargs dirname)
indir="$topdir/submissions"
#outdir="$topdir/data"
submitted="$indir/submitted.txt"

heudiconv_actorid=009

# refresh tokens
# tapis auth tokens refresh

function announce_error() {
	echo TODO: possibly announce that this script failed
}

# TODO: figure out how to do on EXIT with non 0 only
trap announce_error SIGINT SIGHUP SIGABRT 

function skip_file() {
	msg="$1"
	echo "TODO: tapis actors submit announce failed $msg"
}



touch "$submitted"
/bin/ls "$indir"/*/*/*_*[12].zip.MD5SUM | while read f; do
	if grep -q "^$f\$" "$submitted"; then
		echo "$f was submitted, skipping"
		continue
	fi
	(
	 cd "$(dirname $f)";
	 if ! md5sum -c "$f"; then
		# TODO: make it so we avoid announcing twice
		skip_file "md5 mismatch"
		continue
	 fi
        )
	zipfile="${f%.MD5SUM}"
	filename=$(basename "$zipfile" | sed -e 's,.zip,,g')
	subj=${filename%_*}
	ses=${filename#*_}
	#site="$(dirname $zipfile| xargs basename)"
        site_path=$(dirname $(dirname "$zipfile"))
	site="$(basename $site_path)"
	outdir="$site_path/bids/$subj"
	# requires tapis from tapis-cli (pypi)	
	echo tapis actors submit -m "{\"site\": \"$site\", \"subject\": \"$subj\", \"session\": \"$ses\", \"zipfile\": \"$zipfile\", \"outdir\": \"$outdir\"}" "$heudiconv_actorid"
	echo "$f" >> "$submitted"
done
