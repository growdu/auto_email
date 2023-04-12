"""Console script for auto_email."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for auto_email."""
    click.echo("auto_email will start..................")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
