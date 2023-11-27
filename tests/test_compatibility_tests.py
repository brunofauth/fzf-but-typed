from fzf_but_typed.compatibility import SemVer, _test_compatibility
import pytest
import functools


def test_compatibility_test() -> None:
    mock_all_supported_versions = [
        (SemVer(major=0, minor=1, patch=0), SemVer(major=0, minor=1, patch=0)),
        (SemVer(major=0, minor=1, patch=1), SemVer(major=0, minor=2, patch=0)),
        (SemVer(major=0, minor=3, patch=0), SemVer(major=0, minor=3, patch=0)),
        (SemVer(major=1, minor=3, patch=1), SemVer(major=0, minor=4, patch=0)),
    ]

    test1 = functools.partial(
        _test_compatibility,
        latest_supported=mock_all_supported_versions[-1][0],
        all_supported_versions=mock_all_supported_versions,
    )

    with pytest.raises(RuntimeError, match="which is newer"):
        test1(found_version=SemVer(major=2, minor=0, patch=0))

    with pytest.raises(RuntimeError, match="which is older"):
        test1(found_version=SemVer(major=0, minor=0, patch=0))

    with pytest.raises(RuntimeError, match="which is older"):
        test1(found_version=SemVer(major=0, minor=2, patch=0))

    with pytest.raises(RuntimeError, match="has been supported by a previous"):
        test1(found_version=SemVer(major=0, minor=3, patch=0))

    with pytest.raises(SystemExit):
        test1(found_version=SemVer(major=1, minor=3, patch=0))

    with pytest.raises(SystemExit):
        test1(found_version=SemVer(major=1, minor=3, patch=1))

    with pytest.raises(SystemExit):
        test1(found_version=SemVer(major=1, minor=3, patch=2))
