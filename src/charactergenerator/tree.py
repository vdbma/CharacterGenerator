from rich.console import Console
from rich.tree import Tree


def build_tree(conditioning, conditioned):
    root = Tree("[bold]Conditioning[/bold]")

    for entry, weight in zip(conditioning["entries"], conditioning["weights"]):
        branch = root.add(f"[cyan]{entry}[/cyan] [dim]({weight:.2%})[/dim]")

        available = []

        if entry in conditioned:
            available.extend(
                zip(conditioned[entry]["entries"], conditioned[entry]["weights"])
            )

        if None in conditioned:
            available.extend(
                zip(conditioned[None]["entries"], conditioned[None]["weights"])
            )

        total = sum(weight for _, weight in available)

        for name, weight in available:
            probability = weight / total if total else 0
            branch.add(f"[green]{name}[/green] [dim]({probability:.2%})[/dim]")

    return root


def display_tree(conditioning, conditioned):
    console = Console()
    console.print(build_tree(conditioning, conditioned))


def export_mermaid(conditioning, conditioned):
    lines = ["flowchart LR", '    Root["Conditioning"]']

    for i, (entry, weight) in enumerate(
        zip(conditioning["entries"], conditioning["weights"])
    ):
        node = f"C{i}"
        lines.append(f'    Root -->|{weight:.2%}| {node}["{entry}"]')

        available = []

        if entry in conditioned:
            available.extend(
                zip(conditioned[entry]["entries"], conditioned[entry]["weights"])
            )

        if None in conditioned:
            available.extend(
                zip(conditioned[None]["entries"], conditioned[None]["weights"])
            )

        total = sum(w for _, w in available)

        for j, (name, w) in enumerate(available):
            child = f"E{i}_{j}"
            probability = w / total if total else 0

            lines.append(f"    {node} -->|{probability:.2%}| " f'{child}["{name}"]')

    return "\n".join(lines)
