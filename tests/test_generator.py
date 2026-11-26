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
        "first_names": load_table(
            "tests/conditioned_tables/first_names.csv", conditioned=True
        ),
        "last_names": load_table(
            "tests/conditioned_tables/last_names.csv", conditioned=True
        ),
    }
    assert g.conditioning == load_table(
        "tests/conditioned_tables/gender.csv", conditioned=False
    )


def test_format_character():
    character = {"gender": "F", "first_name": "John", "last_name": "Abernathy"}
    assert CharacterGenerator.format_character(None, character) == "F\tJohn\tAbernathy"
