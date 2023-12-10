#! /bin/sh


cd "$(dirname "$0")" || exit 1
env MANWIDTH=80 man fzf > ../fzf-man-pages

