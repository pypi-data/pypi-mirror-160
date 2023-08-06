"""Command-line interface."""
import configparser
import contextlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
from typing import Iterator

import click


@contextlib.contextmanager
def pushd(new_dir: Path) -> Iterator[None]:
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

    Archive a git repo, with submodules.
    """
    if not Path(path).exists():
        click.echo(f"ERROR: {path} does not exist.",err=True)
        sys.exit(1)

    ctx.ensure_object(dict)
    tmpdir = ctx.obj.get("tmpdir", Path(tempfile.mkdtemp()))
    ctx.obj["tmpdir"] = tmpdir
    last_path = None
    if "current_path" in ctx.obj:
        last_path = ctx.obj["current_path"]
        ctx.obj["current_path"] = last_path / path
    else:
        ctx.obj["current_path"] = Path(Path(path).name)

    current_path = ctx.obj["current_path"]

    repo = Path(path).absolute()
    gitmodules_file = repo / ".gitmodules"
    with pushd(repo):

        try:
            subprocess.check_call(["git","rev-parse",ref],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except:
            click.echo(f"ERROR: {ref} is not a valid reference for {path}",err=True)
            sys.exit(2)

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
            os.remove(tmpdir / "current_archive.tar")

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
            output = Path(path).name + "-" + ref + ".zip"
        output_path = Path(output)

        basename = str(output_path.parent / output_path.stem)
        ext = output_path.suffix[1:]
        if ext == "" or ext is None:
            ext = "zip"

        print(f"Writing arvie to {basename}.{ext}")

        shutil.make_archive(basename, ext, tmpdir)


if __name__ == "__main__":
    main(prog_name="git-archive-deep")  # pragma: no cover
