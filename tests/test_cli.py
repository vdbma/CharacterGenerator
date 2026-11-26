from charactergenerator.cli import parse_args
import pytest
from pathlib import Path


def test_parse_args_unconditioned():
    args = parse_args("tests/tables -n 3".split(" "))
    assert args.tables_dir == Path("tests/tables")
    assert args.n == 3
    assert args.conditioning is None
    assert args.sep == "+"
    assert not args.tree
    assert not args.mermaid


def test_parse_args_conditioned():
    args = parse_args("tests/tables -n 3 -c genders.csv".split(" "))
    assert args.tables_dir == Path("tests/tables")
    assert args.n == 3
    assert args.conditioning == "genders.csv"
    assert args.sep == "+"
    assert not args.tree
    assert not args.mermaid


def test_parse_tree_uncoditioned():
    with pytest.raises(SystemExit):
        _args = parse_args("tests/tables --tree".split(" "))


def test_parse_mermaid_uncoditioned():
    with pytest.raises(SystemExit):
        _args = parse_args("tests/tables --mermaid".split(" "))
