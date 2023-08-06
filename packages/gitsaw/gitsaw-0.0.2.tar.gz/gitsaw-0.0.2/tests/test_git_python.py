import pytest
from git import Repo


@pytest.fixture
def repo():
    return Repo("../prune-test")


def test_repo_not_bare(repo):
    assert not repo.bare


def test_repo_has_branches(repo):
    assert len(repo.branches) > 1


def test_repo_list_branches(repo):
    for branch in repo.branches:
        print(branch.name)
