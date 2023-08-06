"""Command-line interface."""
import configparser
import contextlib
import os
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
from typing import Iterator

import click


@contextlib.contextmanager
def pushd(new_dir: pathlib.Path) -> Iterator[None]:
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


@click.command()
@click.version_option()
@click.argument("ref")
@click.argument("path")
@click.option("--output", "-o", help="output file name.")
@click.pass_context
def main(ctx: click.core.Context, ref: str, path: str, output: str) -> None:
    """git-archive-deep

    Archive a git repo with submodules.
    """
    ctx.ensure_object(dict)
    tmpdir = ctx.obj.get("tmpdir", pathlib.Path(tempfile.mkdtemp()))
    ctx.obj["tmpdir"] = tmpdir
    last_path = None
    if "current_path" in ctx.obj:
        last_path = ctx.obj["current_path"]
        ctx.obj["current_path"] = last_path / path
    else:
        ctx.obj["current_path"] = pathlib.Path(pathlib.Path(path).name)

    current_path = ctx.obj["current_path"]

    repo = pathlib.Path(path).absolute()
    gitmodules_file = repo / ".gitmodules"
    with pushd(repo):

        subprocess.run(
            [
                "git",
                "archive",
                "--format",
                "tar",
                ref,
                ".",
                "-o",
                "git-archive-deep-archive.tar",
            ]
        )
        shutil.move("git-archive-deep-archive.tar", tmpdir / "current_archive.tar")
        archive_dir = tmpdir / current_path
        archive_dir.mkdir(exist_ok=True)
        with pushd(archive_dir):
            file = tarfile.open(tmpdir / "current_archive.tar")
            file.extractall(".")
            file.close

        if gitmodules_file.exists():
            gitmodules_config = configparser.ConfigParser()
            gitmodules_config.read(gitmodules_file)
            for section in gitmodules_config:
                if section.startswith("submodule"):
                    mod_path = gitmodules_config[section]["path"]

                    submodule_sha1 = (
                        subprocess.check_output(
                            ["git", "rev-parse", f"{ref}:{mod_path}"]
                        )
                        .decode("utf-8")
                        .strip()
                    )
                    ctx.invoke(main, ref=submodule_sha1, path=mod_path)

    ctx.obj["current_path"] = last_path

    if last_path is None:
        if output is None or output == "":
            output = pathlib.Path(path).name + "-" + ref + ".zip"
        output_path = pathlib.Path(output)

        basename = str(output_path.parent / output_path.stem)
        ext = output_path.suffix[1:]
        if ext == "" or ext is None:
            ext = "zip"

        print(f"Writing arvie to {basename}.{ext}")

        shutil.make_archive(basename, ext, tmpdir)


if __name__ == "__main__":
    main(prog_name="git-archive-deep")  # pragma: no cover
