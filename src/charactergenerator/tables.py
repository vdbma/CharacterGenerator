import csv


def read_csv(path):
    """Read a CSV file and return its rows."""
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        rows = [row for row in reader if row and any(cell.strip() for cell in row)]

    if not rows:
        raise ValueError(f"Empty CSV file: {path}")

    return rows


def parse_weights(values):
    """Convert weights into normalized float probabilities."""

    weights = [float(value) for value in values]

    if not weights:
        raise ValueError("A table must contain at least one weight.")

    if any(weight < 0 for weight in weights):
        raise ValueError("Weights cannot be negative.")

    if all(weight.is_integer() for weight in weights):
        weights = [int(weight) for weight in weights]

        total = sum(weights)

        if total == 0:
            raise ValueError("The sum of weights cannot be zero.")

        return [weight / total for weight in weights]

    if any(weight > 1 for weight in weights):
        raise ValueError(
            "Weights must either all be integers or floats between 0 and 1."
        )

    total = sum(weights)

    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Float weights must sum to 1. Got {total}.")

    return weights


def load_table(path, conditioned=False, numeric_conditions=False):
    """
    Load a CSV table.

    Normal table:
        Entry
        Entry, Weight

    Conditioned table:
        Entry                       (condition = None)
        Entry, Weight                (condition = None)
        Entry, Condition
        Entry, Weight, Condition

    This returns a dict (if no conditions) or a dict of dicts (if conditioned)
    """
    rows = read_csv(path)

    if len(rows) < 2:
        raise ValueError(f"Table must contain a header and entries: {path}")

    rows = rows[1:]

    columns = len(rows[0])

    if not conditioned:
        if columns not in (1, 2):
            raise ValueError(
                f"Invalid table format: {path}, I found {columns} columns but {conditioned = } (expected False)."
            )

        entries = [row[0].strip() for row in rows]

        if columns == 1:
            weights = [1 / len(entries)] * len(entries)
        else:
            weights = parse_weights([row[1].strip() for row in rows])

        return {"entries": entries, "weights": weights}

    if columns not in (1, 2, 3):
        raise ValueError(
            f"Invalid table format: {path}, I found {columns} columns but {conditioned = }."
        )

    # One column: entries without conditions or weights.
    if columns == 1:
        return {
            None: {
                "entries": [row[0].strip() for row in rows],
                "weights": [1 / len(rows)] * len(rows),
            }
        }

    # Two columns:
    # numeric_conditions=True  -> Entry, Condition
    # numeric_conditions=False -> Entry, Weight

    # Two columns: Entry, Weight OR Entry, Condition.
    if columns == 2:
        is_condition = numeric_conditions

        if not is_condition:
            try:
                for row in rows:
                    float(row[1].strip())
            except ValueError:
                is_condition = True

        if is_condition:
            weighted = False
            groups = {}

            for row in rows:
                entry = row[0].strip()
                condition = row[1].strip()

                conditions = (
                    [None]
                    if not condition or condition.lower() == "none"
                    else [c.strip() for c in condition.split("+")]
                )

                for cond in conditions:
                    groups.setdefault(cond, []).append((entry, None))

        else:
            weighted = True
            groups = {None: []}

            for row in rows:
                groups[None].append((row[0].strip(), row[1].strip()))

    # Three columns: Entry, Weight, Condition.
    else:
        groups = {}

        for row in rows:
            entry = row[0].strip()
            weight = row[1].strip()
            condition = row[2].strip()

            conditions = (
                [None]
                if not condition or condition.lower() == "none"
                else [c.strip() for c in condition.split("+")]
            )

            for cond in conditions:
                groups.setdefault(cond, []).append((entry, weight))

        weighted = True

    # Normalize weights independently for each condition.
    result = {}

    for condition, entries in groups.items():
        names = [entry for entry, _ in entries]

        if weighted:
            weights = parse_weights([weight for _, weight in entries])
        else:
            weights = [1 / len(names)] * len(names)

        result[condition] = {"entries": names, "weights": weights}

    return result
