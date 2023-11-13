from __future__ import annotations

import subprocess as sp


def test_compatibility() -> None:
    supported_versions = [
        "0.42.0 (d471067e)",
    ]
    result = sp.run(['fzf', '--version'], capture_output=True, text=True, check=True)
    v = found_version = result.stdout.strip()

    assert found_version in supported_versions, (
        "The contents of this module were written module taking into consideration the man "
        f"pages of fzf version={supported_versions[-1]!r}. You're using fzf version={v!r}. If "
        "that's older than the version I used, some of the features exposed on this API may "
        "not work. Conversely, if the version you're using is newer than mine, some features "
        "you may want to use may be absent here. Regardless of all this, your use case might "
        "probably be supported by this lib. I've included the aformentioned manpages in this "
        "package's repo, so, if you want to be 100% sure, you can download these manpages and "
        "run them through 'diff' with your system's manpages for fzf. See README.md for an "
        "example of how to do this.")

    print("versions are compatible... you're fine!")


if __name__ == "__main__":
    test_compatibility()
