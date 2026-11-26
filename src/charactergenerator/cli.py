import argparse
from pathlib import Path

from .generator import CharacterGenerator
from .tree import display_tree, export_mermaid


def main():
    parser = argparse.ArgumentParser(
        prog="char-gen", description="Generate random characters from CSV tables."
    )

    parser.add_argument("tables_dir", type=Path)

    parser.add_argument(
        "-c", "--conditioning", type=str, help="Name of the conditioning table."
    )

    parser.add_argument(
        "--cn", action="store_true", help="Treat the last column as conditions."
    )

    parser.add_argument(
        "-n", type=int, default=1, help="Number of characters to generate."
    )

    parser.add_argument(
        "--sep", default="+", help="Separator for generated character entries."
    )

    parser.add_argument(
        "--tree", action="store_true", help="Display the conditioning tree."
    )

    parser.add_argument(
        "--mermaid",
        action="store_true",
        help="Export the conditioning tree to Mermaid.",
    )

    args = parser.parse_args()

    if args.n < 1:
        parser.error("-n must be greater than zero.")

    if (args.tree or args.mermaid) and not args.conditioning:
        parser.error("--tree and --mermaid require -c.")

    try:
        generator = CharacterGenerator(
            args.tables_dir,
            conditioning=args.conditioning,
            numeric_conditions=args.cn,
            separator=args.sep,
        )

        if args.tree:
            display_tree(generator.conditioning, generator.conditioned_table)
            return

        if args.mermaid:
            print(export_mermaid(generator.conditioning, generator.conditioned_table))
            return

        characters = generator.generate(args.n)

        for character in characters:
            print(generator.format_character(character))

    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
