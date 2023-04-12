"""Console script for auto_email."""
import sys
import click
import os
from auto_email import auto_email


@click.command()
def main(args=None):
    """Console script for auto_email."""
    click.echo("auto_email will start..................")
    email = auto_email()
    cur_path = os.path.dirname(__file__)
    conf_path = os.path.join(cur_path, 'email.json')
    email.read_config(conf_path)
    #email.loop()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
