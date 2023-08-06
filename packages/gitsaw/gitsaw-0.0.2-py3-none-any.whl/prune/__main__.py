import argparse
from pathlib import Path
import sys
from typing import Any, Dict

from git import GitCommandError, Repo
import inquirer

from prune import __version__

__author__ = "Mads Andreasen"
__copyright__ = "Mads Andreasen"
__license__ = "MIT"


def gitpath(dir: str) -> Path:
    return Path(dir)


def parse_args(args):
    parser = argparse.ArgumentParser(description="Prune git branches")
    parser.add_argument(
        "path",
        type=gitpath,
        help="Path to the git repository",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"prune {__version__}",
    )
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    repo = Repo(args.path)

    for branch in repo.branches:
        question = [
            inquirer.Confirm('delete',
                             message=f'Delete {branch}',
                             default=True)
        ]
        try:
            answer: Dict[Any, Any] | None = inquirer.prompt(question)
            if answer is not None and answer['delete']:
                repo.delete_head(branch, force=True)
        except GitCommandError:
            print(f'Could not delete {branch}')


if __name__ == "__main__":
    main()
