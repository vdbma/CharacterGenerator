from charactergenerator.generator import CharacterGenerator
from charactergenerator.tables import load_table
from pathlib import Path


def test_init_unconditioned():
    g = CharacterGenerator("tests/tables")

    assert g.tables_dir == Path("tests/tables")
    assert g.separator == "+"
    assert g.conditioning_name is None
    assert g.tables == {
        "first_names": load_table("tests/tables/first_names.csv"),
        "last_names": load_table("tests/tables/last_names.csv"),
    }
    assert g.conditioning is None


def test_init_conditioned():
    g = CharacterGenerator("tests/conditioned_tables/", conditioning="gender.csv")

    assert g.tables_dir == Path("tests/conditioned_tables")
    assert g.separator == "+"
    assert g.conditioning_name == "gender.csv"
    assert g.tables == {
        "first_names": {
            "M": {
                "entries": ["John", "Charlie", "Morgan"],
                "weights": [1 / 4, 2 / 4, 1 / 4],
            },
            "F": {
                "entries": ["Mary", "Charlie", "Morgan"],
                "weights": [1 / 4, 2 / 4, 1 / 4],
            },
            "other": {
                "entries": ["Mary", "Charlie", "Morgan"],
                "weights": [1 / 4, 2 / 4, 1 / 4],
            },
        },
        "last_names": {
            "M": {
                "entries": ["Smith", "Abernathy", "Delavoiture", "Swanson"],
                "weights": [5 / 8, 1 / 8, 1 / 8, 1 / 8],
            },
            "F": {
                "entries": ["Smith", "Abernathy", "Delavoiture", "Swanson"],
                "weights": [5 / 8, 1 / 8, 1 / 8, 1 / 8],
            },
            "other": {
                "entries": ["Smith", "Abernathy", "Delavoiture", "Swanson"],
                "weights": [5 / 8, 1 / 8, 1 / 8, 1 / 8],
            },
        },
    }
    assert g.conditioning == load_table(
        "tests/conditioned_tables/gender.csv", conditioned=False
    )


def test_format_character():
    character = {"gender": "F", "first_name": "John", "last_name": "Abernathy"}
    assert CharacterGenerator.format_character(None, character) == "F\tJohn\tAbernathy"


def test_generator_no_explicit_entry():
    """
    Here there is seemingly no possible entry for gender F
    but in fact "Morgan" is a possible entry,
    this should be handled
    """
    g = CharacterGenerator("tests/no_explicit_entry_tables", conditioning="gender.csv")
    assert g.tables == {
        "first_names": {
            "M": {
                "entries": ["John", "Morgan"],
                "weights": [0.0, 1.0],
            },
            "F": {
                "entries": ["Morgan"],
                "weights": [1.0],
            },
        }
    }
