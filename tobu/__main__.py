from functools import partial
from typer import Argument, Option, Typer
from pathlib import Path
import os
import atexit

class State:
    pass


STATE = State()
BASH_COMMANDS = []

atexit.register(lambda: print(*BASH_COMMANDS, sep='\n'))


def bash(text):
    BASH_COMMANDS.extend(t for s in text.splitlines() if (t := s.strip()))


def cd_pytorch():
    bash(f"cd {STATE.root_directory}/pytorch")


app = Typer(
    no_args_is_help=True,
    context_settings={'help_option_names': ['-h', '--help']},
)


def _root_directory():
    path = Path().absolute()
    return path.parent if path.name == 'pytorch' else path


@app.callback()
def tobu(
    dry_run: bool = Option(
        True, '--dry-run', '-d', help='Just print the bash commands, do not execute'
    ),
    root_directory: Path = Option(
        _root_directory(), '--root-directory', '-r', help='Root directory above pytorch'
    ),
    user: str = Option(
        os.environ.get('USER', ''), '--user', '-u', help='Git user name',
    ),
    upstream: str = Option(
        'upstream', '--upstream', '--up', help='The remote for the pytorch/pytorch repo'
    ),
):
    STATE.__dict__.update(locals())



@app.command(help='Clone the repos')
def clone(
    all_: bool = Option(
        False, '--all', '-a', name="_all", help="Update all of the repository, not just pytorch"
    ),
    ref: str = Argument(
        'upstream/viable/strict', help='The ref ID to use'
    ),
    fetch: bool = Option(
        False, '--fetch', '-f', help='Run git fetch on upstream before starting',
    ),
    libraries: str = Option(
        'torchbenchmark,torch-audio,torch-data,torch-vision',
        '--libraries', '-l', help="A list of libraries to clone parallel to pytorch",
    ),
):
    if STATE.user == "pytorch":
        add_remote = ""
    else:
        add_remote = "git remote add upstream git@github.com:pytorch/pytorch.git"

    bash(f"""
        mkdir -p {STATE.root_directory}
        cd {STATE.root_directory}
        git clone git@github.com:${STATE.user}/pytorch.git
        cd pytorch
        git submodule update --init --recursive
        {add_remote}
        cd {STATE.root_directory}"""
    )
    if all_:
        for lib in libraries.split(","):
            bash(f"git clone git@github.com:pytorch/{lib}.git")


@app.command(help='')
def update(
    all_: bool = Option(
        False, '--all', '-a', name="_all", help="Update all of the repository, not just pytorch"
    ),
    ref: str = Argument(
        'upstream/viable/strict', help='The ref ID to use'
    ),
):
    pass


@app.command(help='')
def env(
):
    pass



@app.command(help='')
def set(
):
    pass


@app.command(help='')
def build(
    all: bool = False,
):
    pass



@app.command(help='')
def clean(
    all: bool = False,
):
    pass


if __name__ == '__main__':
    app()
