from typer import Argument, Option, Typer
from pathlib import Path
import os

STATE = object()

app = typer.Typer(
    no_args_is_help=True,
    context_settings={'help_option_names': ['-h', '--help']},
)


def _root_directory():
    path = Path().absolute()
    return path.parent if path.name == 'pytorch' else path


@app.callback
def callback(
    all: bool = Option(
        False, '--all', '-a', help="Update all of the repository, not just pytorch"
    ),
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
    ref: str = Argument(
        'upstream/viable/strict', '--ref', '-r', help='The ref ID to use'
    ),
    fetch: bool = Option(
        False, '--fetch', '-f', help='Run git fetch on upstream before starting',
    ),
    libraries: str = Option(
        'torchbenchmark,torch-data,torch-data,torch-vision',
        '--libraries', '-l', help="A list of libraries to clone parallel to pytorch",
):
    def clone():
        STATE.root_directory.mkdir(exist_ok=True, parents=True)
        yield f"cd {STATE.root_directory}"
        yield f"git clone git@github.com:{STATE.user} pytorch"



@app.command(help='')
def update(
    ref: str = Argument(
        'TODO', '--ref', '-r', help='The ref ID to use'
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
