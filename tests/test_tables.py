from charactergenerator.tables import read_csv, load_table, parse_weights


def test_read_csv():
    read_table = read_csv("tests/tables/first_names.csv")
    assert read_table == [["John", " 1"], ["Mary", " 1"], ["Charlie", " 2"]]


def test_load_table_unconditioned():
    read_table = load_table("tests/tables/first_names.csv")
    assert read_table == {
        "entries": ["John", "Mary", "Charlie"],
        "weights": [1 / 4, 1 / 4, 1 / 2],
    }


def test_load_table_conditioned():
    read_table = load_table(
        "tests/conditioned_tables/first_names.csv", conditioned=True
    )
    assert read_table == {
        "M": {"entries": ["John", "Charlie"], "weights": [1 / 3, 2 / 3]},
        "F": {"entries": ["Mary", "Charlie"], "weights": [1 / 3, 2 / 3]},
        "other": {"entries": ["Mary", "Charlie"], "weights": [1 / 3, 2 / 3]},
    }


def test_parse_weights_unconditioned():
    read_table = read_csv("tests/tables/first_names.csv")
    weights = parse_weights([row[1].strip() for row in read_table])
    assert weights == [1 / 4, 1 / 4, 1 / 2]


def test_parse_weights_conditioned():
    read_table = read_csv("tests/conditioned_tables/first_names.csv")
    weights = parse_weights([row[1].strip() for row in read_table])
    assert weights == [1 / 4, 1 / 4, 1 / 2]
