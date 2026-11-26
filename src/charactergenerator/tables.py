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
        Entry                       (applies to all conditions)
        Entry, Weight                (applies to all conditions)
        Entry, Condition
        Entry, Weight, Condition

    Entries with no condition are appended to every existing condition.
    """

    rows = read_csv(path)

    if len(rows) < 1:
        raise ValueError(f"Table must contain entries: {path}")

    columns = len(rows[0])

    # Normal table
    if not conditioned:
        if columns not in (1, 2):
            raise ValueError(f"Invalid table format: {path}")

        entries = [row[0].strip() for row in rows]

        if columns == 1:
            weights = [1 / len(entries)] * len(entries)
        else:
            weights = parse_weights([row[1].strip() for row in rows])

        return {"entries": entries, "weights": weights}

    if columns not in (1, 2, 3):
        raise ValueError(f"Invalid conditioned table format: {path}")

    groups = {}
    unconditional = []

    # One column: every entry applies to every condition.
    if columns == 1:
        unconditional = [(row[0].strip(), None) for row in rows]

    # Two columns: automatically detect weights or conditions.
    elif columns == 2:
        is_condition = numeric_conditions

        if not is_condition:
            try:
                for row in rows:
                    float(row[1].strip())
            except ValueError:
                is_condition = True

        if is_condition:
            for row in rows:
                entry = row[0].strip()
                condition = row[1].strip()

                conditions = (
                    []
                    if not condition or condition.lower() == "none"
                    else [c.strip() for c in condition.split("+")]
                )

                if not conditions:
                    unconditional.append((entry, None))
                else:
                    for cond in conditions:
                        groups.setdefault(cond, []).append((entry, None))

        else:
            unconditional = [(row[0].strip(), row[1].strip()) for row in rows]

    # Three columns: Entry, Weight, Condition.
    else:
        for row in rows:
            entry = row[0].strip()
            weight = row[1].strip()
            condition = row[2].strip()

            conditions = (
                []
                if not condition or condition.lower() == "none"
                else [c.strip() for c in condition.split("+")]
            )

            if not conditions:
                unconditional.append((entry, weight))
            else:
                for cond in conditions:
                    groups.setdefault(cond, []).append((entry, weight))

    # If there are no explicit conditions, create a default category.
    if not groups:
        groups[None] = unconditional

    else:
        # Append unconditional entries to every condition.
        for condition in groups:
            groups[condition].extend(unconditional)

    # Normalize weights independently for every condition.
    result = {}

    for condition, entries in groups.items():
        names = [entry for entry, _ in entries]

        if not names:
            raise ValueError(f"No entries for condition: {condition}")

        if entries[0][1] is None:
            weights = [1 / len(names)] * len(names)
        else:
            weights = parse_weights([weight for _, weight in entries])

        result[condition] = {"entries": names, "weights": weights}

    return result
