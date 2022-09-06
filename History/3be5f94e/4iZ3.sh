#!/bin/bash
# This software is public domain.
# For more information, please refer to <http://unlicense.org>

# BASE
# LOCAL
# REMOTE
# MERGED

ca=$1
lh=$2
rh=$3
merged=$4

cleanup=()
trap 'rm -f "${cleanup[@]}"' EXIT

cat "$lh" > "$merged"
{
	echo '# LOCAL DIFF'
	diff -u "$ca" "$lh"
} > "$lh.diff"
{
	echo '# REMOTE DIFF'
	diff -u "$ca" "$rh"
} > "$rh.diff"

diff -u "$ca" "$rh" | \
	patch --version-control=never --force --fuzz=0 --reject-format=unified "$merged" 1>/dev/null

cleanup+=("$lh.diff" "$rh.diff" "$merged.rej")

args=()
if (($(wc -l < "$merged.rej")0 < $(wc -l < "$lh.diff")0)); then
	args+=(-c "vsplit $merged")
	args+=(-c "wincmd w | split $merged.rej  | 0r !git log -1 $(< .git/MERGE_HEAD)" -c "f Chunks\ left\ to\ merge | set buftype=nofile | set filetype=diff")
	args+=(-c "wincmd w | split $lh.diff    | f Changes\ that\ caused\ conflict | set buftype=nofile | set filetype=diff")
	if [[ -e .git/rebase-merge ]]; then
		args+=(-c "wincmd w | set buftype=nofile | r !git show $(< .git/rebase-merge/stopped-sha)"  -c "f 'git show $(< .git/rebase-merge/stopped-sha)'")
	else
		args+=(-c "wincmd w | set buftype=nofile | r !git log --merge -p $merged"  -c "f 'git log --merge -p $merged'")
	fi
	args+=(-c "set filetype=git | 0")
	args+=(-c "wincmd t")
else
	cat "$lh" > "$merged"
	patch -R --force --fuzz=0 --reject-format=unified "$merged" 1>/dev/null < "$lh.diff"
	diff -u "$ca" "$rh" | \
		patch --force --fuzz=0 --reject-format=unified "$merged" 1>/dev/null
	args+=(-c "vsplit $merged")
	args+=(-c "wincmd w" -c "e $lh.diff")
	args+=(-c "set filetype=diff")
	args+=(-c "wincmd t")
fi

if ! vim "${args[@]}"; then
	exit 1
fi

while :; do
	read -ep "Was the merge successful? [y/n] "
	if [[ $REPLY == y ]]; then
		exit 0
	else
		cp "$merged" "$merged.work_in_progress"
		exit 1
	fi
done