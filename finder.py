import click
from pathlib import Path
from utils import find_by_name, find_by_ext, find_by_mod, timestamp_to_string
from datetime import datetime

def option_search(path, key, value):
    search_mapping = {
        "name": find_by_name,
        "ext": find_by_ext,
        "mod": find_by_mod
    }

    files = search_mapping[key](path, value)
    if not files:
        click.echo(f"No file with {key} {value} was found.")
    else:
        for f in files:
            click.echo(
                f"Name:{f.stem}\nExtension:{f.suffix}\nModified: {timestamp_to_string(f.stat().st_mtime)}\nLocation: {f.parent.absolute()}")


@click.command()
@click.argument("path", default="")
@click.option("-k", "--key", required=True, type=click.Choice(["name", "ext", "mod"]))
@click.option("-v", "--value", required=True)
def finder(path, key, value):
    root = Path(path)
    if not root.is_dir():
        raise Exception("The path is not a directory")

    click.echo(f"The directory selected directory was: {root.absolute()}")

    # pesquisa
    option_search(path=root,key=key, value=value)



finder()
