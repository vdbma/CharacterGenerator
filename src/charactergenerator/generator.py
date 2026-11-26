import random
from pathlib import Path
from .tables import load_table
import copy


class CharacterGenerator:
    def __init__(
        self, tables_dir, conditioning=None, numeric_conditions=False, separator="+"
    ):
        self.tables_dir = Path(tables_dir)
        self.separator = separator
        self.conditioning_name = conditioning

        if not self.tables_dir.is_dir():
            raise ValueError(f"Directory does not exist: {tables_dir}")

        self.tables = {}
        self.conditioning = None

        for path in sorted(self.tables_dir.glob("*.csv")):
            if conditioning and path.name == Path(conditioning).name:
                self.conditioning = load_table(path, conditioned=False)
                continue

            self.tables[path.stem] = load_table(
                path,
                conditioned=bool(conditioning),
                numeric_conditions=numeric_conditions,
            )

        if conditioning and self.conditioning is None:
            raise ValueError(f"Conditioning table not found: {conditioning}")

        if conditioning is not None:
            self.complete_tables()

    def complete_tables(self):
        """
        This completes the tables for items with no condition
        """
        completed_table = {}
        for conditioned_option in self.tables.keys():
            completed_table[conditioned_option] = {}
            # add conditions that were not use in this table
            for cond in self.conditioning["entries"]:
                if cond is not None:
                    if cond in self.tables[conditioned_option]:
                        completed_table[conditioned_option][cond] = copy.deepcopy(
                            self.tables[conditioned_option][cond]
                        )
                    else:
                        completed_table[conditioned_option][cond] = copy.deepcopy(
                            self.tables[conditioned_option][None]
                        )
        self.tables = completed_table

    @staticmethod
    def choose(table, condition=None):
        """Choose an entry from a normal or conditioned table."""

        # Normal table
        if "entries" in table:
            return random.choices(table["entries"], weights=table["weights"], k=1)[0]

        # Conditioned table
        available = []

        if condition in table:
            available.append(table[condition])

        if None in table:
            available.append(table[None])

        if not available:
            raise ValueError(f"No entries available for condition: {condition}")

        entries = []
        weights = []

        for group in available:
            entries.extend(group["entries"])
            weights.extend(group["weights"])

        return random.choices(entries, weights=weights, k=1)[0]

    def generate_one(self):
        result = {}

        # Pick the initial condition
        condition = None
        if self.conditioning is not None:
            condition = self.choose(self.conditioning)

            # Store condition first
            result["conditioning"] = condition

        # Generate entries from all tables
        for name, table in self.tables.items():
            result[name] = self.choose(table, condition)

        return result

    def generate(self, number=1):
        return [self.generate_one() for _ in range(number)]

    def format_character(self, character):
        return "\t".join(str(value) for value in character.values())
