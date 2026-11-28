import argparse
from pathlib import Path
import sys
import pyperclip

from .generator import CharacterGenerator
from .tree import display_tree, export_mermaid


def parse_args(sys_args):
    parser = argparse.ArgumentParser(
        prog="char-gen",
        description="Generate random characters from CSV tables.",
        epilog="The generated character list is automatically add to clipboard.",
    )
    parser.add_argument(
        "tables_dir",
        type=Path,
        default=Path("./"),
        nargs="?",
    )

    parser.add_argument(
        "-c",
        "--conditioning",
        type=str,
        help=" The name of the conditioning table found in the TABLES_DIR folder.",
    )

    parser.add_argument(
        "--cn",
        action="store_true",
        help="Treat the last column as conditions. Must be used if CONDITIONING_TABLE uses numbers as entries.",
    )

    parser.add_argument(
        "-n", type=int, default=1, help="Number of characters to generate."
    )

    parser.add_argument(
        "--sep",
        default="+",
        help="Sets the new character to separated conditionned entries. Default is '+'.",
    )

    parser.add_argument(
        "--tree",
        action="store_true",
        help="Display the conditioning tree. Can't be used withtout conditioning.",
    )

    parser.add_argument(
        "--mermaid",
        action="store_true",
        help="Export the conditioning tree to Mermaid. Can't be used withtout conditioning. Mermaid code is automatically added to clipboard.",
    )

    args = parser.parse_args(sys_args)
    if args.n < 1:
        parser.error("-n must be greater than zero.")

    if (args.tree or args.mermaid) and not args.conditioning:
        parser.error("--tree and --mermaid don't make sense without conditioning.")
    return args


def print_and_add_to_clipboard(s):
    pyperclip.copy(s)
    print(s)


def main():
    args = parse_args(sys.argv[1:])

    try:
        generator = CharacterGenerator(
            args.tables_dir,
            conditioning=args.conditioning,
            numeric_conditions=args.cn,
            separator=args.sep,
        )

        if args.tree:
            display_tree(generator.conditioning, generator.tables)

        if args.mermaid:
            print_and_add_to_clipboard(
                export_mermaid(generator.conditioning, generator.tables)
            )

        if args.mermaid or args.tree:
            return

        characters = generator.generate(args.n)

        print_and_add_to_clipboard(
            "\n".join(
                [generator.format_character(character) for character in characters]
            )
        )

    except (ValueError, OSError) as error:
        args.error(str(error))


if __name__ == "__main__":
    main()
