import click
from pathlib import Path
from utils import find_by_name, find_by_ext, find_by_mod, timestamp_to_string, get_folders, get_files_details
import shutil
from datetime import datetime
from tabulate import tabulate
def option_search(path, key, value, recursive):
    search_mapping = {
        "name": find_by_name,
        "ext": find_by_ext,
        "mod": find_by_mod
    }
    files = search_mapping[key](path, value)
    if recursive:
        subdirs = get_folders(path)
        for subdir in subdirs:
            files += option_search(subdir, key, value, recursive)
    return files

def process_results(files, key, value):

    if not files:
        click.echo(f"No file with {key} {value} was found.")
    else:
        table_data = get_files_details(files)
        table_headers = ["Name", "Ext", "Mod", "Location"]
        tabulated_data = tabulate(tabular_data=table_data, headers=table_headers, tablefmt="pipe")
        click.echo(tabulated_data)
        return tabulated_data


@click.command()
@click.argument("path", default="")
@click.option("-k", "--key", required=True, type=click.Choice(["name", "ext", "mod"]))
@click.option("-v", "--value", required=True)
@click.option("-r", "--recursive", is_flag=True, default=False)
@click.option("-s", "--save", is_flag=True, default=False)
@click.option("-c", "--copy-to")
def finder(path, key, value, recursive, copy_to, save):
    root = Path(path)
    if not root.is_dir():
        raise Exception("The path is not a directory")

    click.echo(f"The directory selected directory was: {root.absolute()}")

    # pesquisa
    files = option_search(path=root,key=key, value=value, recursive=recursive)
    report = process_results(files=files, key=key,value=value)
    if save:
        if report:
            report_file_path = root / f"report_{datetime.now().strftime('%d%m%Y')}.txt"
            with open(report_file_path.absolute() , mode="w") as report_file:
                report_file.write(report)




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
