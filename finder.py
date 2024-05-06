import click
from pathlib import Path
from utils import find_by_name, find_by_ext, find_by_mod, timestamp_to_string, get_folders
import shutil
from datetime import datetime

def option_search(path, key, value, recursive):
    search_mapping = {
        "name": find_by_name,
        "ext": find_by_ext,
        "mod": find_by_mod
    }
    files = search_mapping[key](path, value)
    if recursive:
        subdirs = get_folders( )
        for subdir in subdirs:
            files += option_search(subdir, key, value, recursive)
    return files

def show_files(key,value,files):
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
@click.option("-r", "--recursive", is_flag=True, default=False)
@click.option("-c", "--copy-to")
def finder(path, key, value, recursive, copy_to):
    root = Path(path)
    if not root.is_dir():
        raise Exception("The path is not a directory")

    click.echo(f"The directory selected directory was: {root.absolute()}")

    # pesquisa
    files = option_search(path=root,key=key, value=value, recursive=recursive)
    show_files(key,value,files)

    if copy_to:
        copy_path = Path(copy_to)
        if not copy_path.is_dir():
            copy_path.mkdir(parents=True)
        for file in files:
            dst_file = copy_path / file.name
            if dst_file.is_file():
                dst_file = copy_path / f"{file.stem}_{datetime.now().strftime('%d%m%Y%H%M%S%f')}{file.suffix}"
            shutil.copy(src=file.absolute(), dst=dst_file)


finder()
