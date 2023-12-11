#! /usr/bin/env python3

from pprint import pprint
import difflib
import subprocess as sp
import tempfile as tf
import funparse.api as fp
from chitter import ChainableIter
from collections import OrderedDict
from collections.abc import Iterable
import typing
from typing import Callable, ParamSpec, TypeVar, TextIO

P = ParamSpec('P')
T = TypeVar('T')


# yapf: disable
def chainable(func: Callable[P, Iterable[T]]) -> Callable[P, ChainableIter[T]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> ChainableIter[T]:
        return ChainableIter(func(*args, **kwargs))
    return wrapper
# yapf: enable


def get_options_lines(file_path: str) -> tuple[str, list[str]]:
    with open(file_path) as file:
        # yapf: disable
        contents = iter(file)
        version_line = ChainableIter(contents).drop_while(lambda l: not l.startswith('.TH')).first()
        return version_line, (ChainableIter(contents)
            .drop_while(lambda l: not l.startswith('.SH OPTIONS'))
            .drop(1).take_while(lambda l: not l.startswith(".SH"))
            .to_list()
        )
        # yapf: enable


@chainable
def split_by_category(lines: list[str]) -> Iterable[tuple[str, list[str]]]:
    section_name: str = ""
    batch = []
    for line in lines:
        if not line.startswith('.SS'):
            batch.append(line)
            continue
        yield section_name, batch
        section_name = line[4:].rstrip('\n\r')
        batch = []
    yield section_name, batch


def diff_files(
    file_path_1: str,
    file_path_2: str,
) -> str | None:
    process = sp.run(
        ['diff', '--color=always', file_path_1, file_path_2],
        text=True,
        stdout=sp.PIPE,
    )

    # yapf: disable
    match process.returncode:
        case 0: return None
        case 1: return process.stdout
        case _:
            process.check_returncode()
            assert False, "unreachable"
    # yapf: enable


def diff_lines(
    lines1: list[str],
    lines2: list[str],
) -> str | None:
    with tf.NamedTemporaryFile('r+') as f1, tf.NamedTemporaryFile('r+') as f2:
        f1.writelines(lines1)
        f1.flush()
        f2.writelines(lines2)
        f2.flush()
        return diff_files(f1.name, f2.name)


def get_systems_manpages() -> tf._TemporaryFileWrapper:
    file = tf.NamedTemporaryFile('w')
    file.write(
        sp.run(
            ['gunzip', '--stdout', '/usr/share/man/man1/fzf.1.gz'],
            check=True,
            text=True,
            stdout=sp.PIPE,
        ).stdout)
    file.flush()

    return file


@fp.as_arg_parser
def cli(
    file_path_old: str,
    file_path_new: str | None = None,
) -> None:
    if file_path_new is not None:
        return top_level_diff(file_path_old, file_path_new)

    with get_systems_manpages() as new:
        return top_level_diff(file_path_old, new.name)


def top_level_diff(
    file_path_old: str,
    file_path_new: str,
) -> None:
    old_version, old_opt_lines = get_options_lines(file_path_old)
    old_opt_by_categ = split_by_category(old_opt_lines).drop(1).collect(OrderedDict)
    old_opt_categ = set(old_opt_by_categ.keys())

    new_version, new_opt_lines = get_options_lines(file_path_new)
    new_opt_by_categ = split_by_category(new_opt_lines).drop(1).collect(OrderedDict)
    new_opt_categ = set(new_opt_by_categ.keys())

    print("# VERSION DIFF")
    print(diff_lines([old_version], [new_version]), '\n\n')

    if len(added := new_opt_categ - old_opt_categ) != 0:
        print("# CATEGORIES ADDED (not gonna diff):")
        print('\n'.join(f'--> {categ}' for categ in added), '\n\n')

    if len(removed := old_opt_categ - new_opt_categ) != 0:
        print("# CATEGORIES REMOVED (not gonna diff):")
        print('\n'.join(f'--> {categ}' for categ in removed), '\n\n')

    for categ in old_opt_categ & new_opt_categ:
        if (diff := diff_lines(old_opt_by_categ[categ], new_opt_by_categ[categ])) is not None:
            print(f"# DIFF FOR {categ!r}")
            print(diff, '\n\n')


def main():
    cli.run(None)   # type: ignore


if __name__ == "__main__":
    main()
