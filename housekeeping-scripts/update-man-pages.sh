#! /bin/sh


cd "$(dirname "$0")" || exit 1

if ! gunzip --stdout /usr/share/man/man1/fzf.1.gz > ../fzf.1.man; then
    >&2 echo "Couldn't update fzf manpages ('fzf.1.man')"
    exit 1
fi

