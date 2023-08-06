"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """LIWC Trie."""


if __name__ == "__main__":
    main(prog_name="liwc-trie")  # pragma: no cover
