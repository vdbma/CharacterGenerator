from charactergenerator.cli import parse_args, print_and_add_to_clipboard
import pytest
from pathlib import Path
import pyperclip


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


def test_print_and_add_to_clipboard(capsys):
    s = "Loremp ipsum dolor sit amet"
    print_and_add_to_clipboard(s)
    captured = capsys.readouterr()
    assert captured.out == s + "\n"
    assert pyperclip.paste() == s


def test_print_and_add_to_clipboard_kwargs(capsys):
    s = "Loremp ipsum dolor sit amet"
    print_and_add_to_clipboard(s, end=".")
    captured = capsys.readouterr()
    assert captured.out == s + "."
    assert pyperclip.paste() == s
