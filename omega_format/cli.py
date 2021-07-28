import sys
from pathlib import Path
from typing import Optional

import typer

sys.path.append(str(Path(__file__).parent.parent.resolve()))
from omega_format.reference_recording import ReferenceRecording
from omega_format.perception_recording import PerceptionRecording
from omega_format.enums import generate_enums
from pathlib import Path

import importlib.util

visualization_available = importlib.util.find_spec("PyQt5") is not None and \
    importlib.util.find_spec("pyqtgraph") is not None

app = typer.Typer()


def get_snippets_for_vis(reference, perception, snip, max_snippets):
    validate = False
    if reference is not None:
        rr = ReferenceRecording.from_hdf5(reference, validate)
        if snip and perception is None:
            snippets = [SnippetContainer(reference=snippet) for snippet in rr.extract_snippets(max_snippets)]
        elif perception is not None:
            snippets = [SnippetContainer(perception=PerceptionRecording.from_hdf5(perception, validate), reference=rr)]
        else:
            snippets = [SnippetContainer(reference=rr)]
    elif perception is not None:
        snippets = [SnippetContainer(perception=PerceptionRecording.from_hdf5(perception, validate))]
    else:
        raise ValueError('Either define a reference filename or a perception filename')
    return snippets


if visualization_available:
    from omega_format.visualization.visualizer import Visualizer, SnippetContainer

    @app.command("visualize")
    def visualize(reference: Optional[Path] = typer.Argument(None, exists=True, readable=True, dir_okay=False),
                  perception: Optional[Path] = typer.Option(None, exists=True, readable=True, dir_okay=False),
                  snip: bool = typer.Option(False),
                  max_snippets: Optional[int] = typer.Option(2)):
        """
        Visualizes data of `ReferenceRecording` and `PerceptionRecording` files.
        """

        snippets = get_snippets_for_vis(reference, perception, snip, max_snippets)
        title = f'Perception: {perception.stem} ' if perception is not None else ''
        title += f'Reference: {reference.stem}' if reference is not None else ''
        visualizer = Visualizer(snippets, title)
        visualizer.start_gui_and_visualization()
else:
    @app.command("visualize")
    def visualize():
        """
        You need to install `pyqtgraph` and `PyQt5` to use this function (Visualize an ReferenceRecording).
        """
        raise ModuleNotFoundError('You need to install `pyqtgraph` and `PyQt5` to use this function (Visualize an ReferenceRecording).')


@app.command("verify")
def verify(reference: Optional[Path] = typer.Option(None, exists=True, readable=True, dir_okay=False),
           perception: Optional[Path] = typer.Option(None, exists=True, readable=True, dir_okay=False)):
    """
    Test if a OMEGA Format file conforms to specification
    """
    if reference is not None:
        try:
            rr = ReferenceRecording.from_hdf5(reference)
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise ValueError('An error occurred while trying to read the reference recording file. '
                            'Make sure it conforms to the OMEGA Format reference recording format. '
                            'If you are sure it does, please file an issue.') from e
        else: 
            typer.echo(typer.style(f'The OMEGA Format reference file {reference} conforms to the specification and passes basic sanity checks.', fg=typer.colors.GREEN, bold=True))


    if perception is not None:
        try:
            pr = PerceptionRecording.from_hdf5(perception)
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise ValueError('An error occurred while trying to read the perception recording file. '
                             'Make sure it conforms to the OMEGA Format perception recording format. '
                             'If you are sure it does, please file an issue.') from e
        else: 
            typer.echo(typer.style(f'The OMEGA Format perception file {reference} conforms to the specification and passes basic sanity checks.', fg=typer.colors.GREEN, bold=True))


@app.command("version")
def version():
    """
        Returns the version of the OMEGA Format
    """
    import omega_format
    print(omega_format.__version__)
    return omega_format.__version__


@app.command("clean-version")
def version():
    """
        Returns the clean version of the OMEGA Format
    """
    import omega_format
    print(omega_format.__clean_version__)
    return omega_format.__clean_version__


@app.command('generate_c_headers_and_json', help='Generate .h and .json from python enums.')
def _generate_enums():
    generate_enums()


if __name__ == "__main__":
    app()
