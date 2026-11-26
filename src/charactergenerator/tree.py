from rich.console import Console
from rich.tree import Tree


def build_tree(conditioning, tables):
    """
    Build a tree representing all possible character combinations.

    Parameters
    ----------
    conditioning : dict | None
        The initial conditioning table.
    tables : dict
        Dictionary of table names and their contents.
        Tables can be either normal or conditioned.
    """

    root = Tree("[bold]Character Generator[/bold]")

    # No conditioning: display all tables independently
    if conditioning is None:
        for name, table in tables.items():
            branch = root.add(f"[bold cyan]{name}[/bold cyan]")

            for entry, weight in zip(table["entries"], table["weights"]):
                branch.add(f"[green]{entry}[/green] [dim]({weight:.2%})[/dim]")

        return root

    # Conditioning table
    for condition, condition_weight in zip(
        conditioning["entries"], conditioning["weights"]
    ):
        condition_branch = root.add(
            f"[bold cyan]{condition}[/bold cyan] "
            f"[dim]({condition_weight:.2%})[/dim]"
        )

        # Iterate over all other tables
        for name, table in tables.items():
            table_branch = condition_branch.add(f"[bold yellow]{name}[/bold yellow]")

            # Normal table
            if "entries" in table:
                entries = table["entries"]
                weights = table["weights"]

            # Conditioned table
            else:
                available = []

                if condition in table:
                    available.append(table[condition])

                if None in table:
                    available.append(table[None])

                if not available:
                    table_branch.add("[red]No available entries[/red]")
                    continue

                entries = []
                weights = []

                for group in available:
                    entries.extend(group["entries"])
                    weights.extend(group["weights"])

                total = sum(weights)
                weights = [w / total for w in weights]

            for entry, weight in zip(entries, weights):
                table_branch.add(
                    f"[green]{entry}[/green] " f"[dim]({weight:.2%})[/dim]"
                )

    return root


def display_tree(conditioning, tables):
    console = Console()
    console.print(build_tree(conditioning, tables))


def export_mermaid(conditioning, tables):
    """Export the complete character generation tree to Mermaid."""

    lines = ["flowchart LR", '    Root["Character Generator"]']

    if conditioning is None:
        for i, (name, table) in enumerate(tables.items()):
            table_node = f"T{i}"

            lines.append(f'    Root --> {table_node}["{name}"]')

            for j, (entry, weight) in enumerate(
                zip(table["entries"], table["weights"])
            ):
                node = f"E{i}_{j}"
                lines.append(
                    f"    {table_node} -->|{weight:.2%}| " f'{node}["{entry}"]'
                )

        return "\n".join(lines)

    for i, (condition, condition_weight) in enumerate(
        zip(conditioning["entries"], conditioning["weights"])
    ):
        condition_node = f"C{i}"

        lines.append(
            f"    Root -->|{condition_weight:.2%}| " f'{condition_node}["{condition}"]'
        )

        for j, (name, table) in enumerate(tables.items()):
            table_node = f"T{i}_{j}"

            lines.append(f"    {condition_node} --> " f'{table_node}["{name}"]')

            if "entries" in table:
                entries = table["entries"]
                weights = table["weights"]
            else:
                available = []

                if condition in table:
                    available.append(table[condition])

                if None in table:
                    available.append(table[None])

                entries = []
                weights = []

                for group in available:
                    entries.extend(group["entries"])
                    weights.extend(group["weights"])

                total = sum(weights)
                weights = [w / total for w in weights] if total else []

            for k, (entry, weight) in enumerate(zip(entries, weights)):
                node = f"E{i}_{j}_{k}"

                lines.append(
                    f"    {table_node} -->|{weight:.2%}| " f'{node}["{entry}"]'
                )

    return "\n".join(lines)
