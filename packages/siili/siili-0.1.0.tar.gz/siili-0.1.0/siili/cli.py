# -*- coding: utf-8 -*-
import click

import siili.filework as filework


@click.group()
@click.option(
    "-v", "--verbosity", default=1, type=int, help="Set verbosity [1-3]", count=True
)
def cli(verbosity: int) -> None:
    # click.echo(f"verbosity: {min(verbosity, 3)} / 3")
    pass


@click.command()
@click.argument(
    "file",
    type=click.File(mode="r", encoding=None, errors="strict", atomic=False),
)
def upload(file: click.File) -> None:
    """Upload a file to Amazon S3. Uses defaults from .env file."""
    # click.echo(f"Preparing for upload: {file.name}")
    filework.upload(file.name)


@click.command()
def list_buckets() -> None:
    """List all S3 buckets."""
    click.echo("Listing buckets.")


@click.command()
def get_current_bucket() -> None:
    """Get the S3 bucket we're currently dumping into."""
    click.echo("Listing buckets.")


@click.command()
def set_current_bucket() -> None:
    """Set the S3 bucket to dump into."""
    click.echo("Listing buckets.")


@click.command()
@click.option("--verbose", "-v", help="Increase verbosity")
def set_verbosity(verbose: int) -> None:
    # click.echo(f"Verbosity: {verbose}")
    pass


cli.add_command(upload)
cli.add_command(list_buckets, name="list")
cli.add_command(get_current_bucket, name="get")
cli.add_command(set_current_bucket, name="set")

if __name__ == "__main__":
    cli()
