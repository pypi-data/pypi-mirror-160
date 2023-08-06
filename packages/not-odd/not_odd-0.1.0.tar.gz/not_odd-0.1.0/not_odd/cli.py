"""Console script for not_odd."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for not_odd."""
    click.echo("Replace this message by putting your code into "
               "not_odd.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
