#! /bin/sh


tmp_file="$(mktemp --tmpdir)"
env MANWIDTH=80 man fzf > "$tmp_file"

cd "$(dirname "$0")" || exit 1

diff --color=always \
    "$(cat ../fzf-man-pages | sed -e 's|\s\s\+| |g' | procsub)" \
    "$(cat "$tmp_file" | sed -e 's|\s\s\+| |g' | procsub)"

rm "$tmp_file"

