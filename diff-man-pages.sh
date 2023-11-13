#! /bin/sh


tmp_file="$(mktemp --tmpdir)"
man fzf > "$tmp_file"

cd "$(dirname "$0")" || exit 1

diff --color=always ./fzf-man-pages "$tmp_file"
rm "$tmp_file"

