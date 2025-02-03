import sys
from pathlib import Path
from typing import Optional

import typer

sys.path.append(str(Path(__file__).parent.parent.resolve()))
from omega_format.reference_recording import ReferenceRecording
from omega_format.perception_recording import PerceptionRecording
from omega_format.enums import generate_enums
from pathlib import Path
from omega_format.converters.from_asam_opendrive import convert_odr_app
from omega_format.converters.from_level_x_like import app as levelx_app
import importlib.util

visualization_available = importlib.util.find_spec("PyQt5") is not None and \
    importlib.util.find_spec("pyqtgraph") is not None

app = typer.Typer(pretty_exceptions_show_locals=False)


def get_snippets_for_vis(reference, perception, snip, max_snippets, legacy=None):
    validate = True
    if reference is not None:
        rr = ReferenceRecording.from_hdf5(reference, validate, legacy=legacy)
        if snip and perception is None:
            snippets = [SnippetContainer(reference=snippet) for snippet in rr.extract_snippets(max_snippets)]
        elif perception is not None:
            snippets = [SnippetContainer(perception=PerceptionRecording.from_hdf5(perception, validate), reference=rr)]
        else:
            snippets = [SnippetContainer(reference=rr)]
    elif perception is not None:
        snippets = [SnippetContainer(perception=PerceptionRecording.from_hdf5(perception, validate, legacy=legacy))]
    else:
        raise ValueError('Either define a reference filename or a perception filename')
    return snippets


if visualization_available:
    from omega_format.visualization.visualizer import Visualizer, SnippetContainer

    @app.command("visualize")
    def visualize(reference: Optional[Path] = typer.Argument(None, exists=True, readable=True, dir_okay=False),
                  perception: Optional[Path] = typer.Option(None, exists=True, readable=True, dir_okay=False),
                  snip: bool = typer.Option(False),
                  max_snippets: Optional[int] = typer.Option(2), legacy: Optional[str] = typer.Option(None)):
        """
        Visualizes data of `ReferenceRecording` and `PerceptionRecording` files.
        """

        snippets = get_snippets_for_vis(reference, perception, snip, max_snippets, legacy=legacy)
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
           perception: Optional[Path] = typer.Option(None, exists=True, readable=True, dir_okay=False),
           legacy: Optional[str] = typer.Option(None)):
    """
    Test if a OMEGAFormat file conforms to specification
    """
    if reference is not None:
        try:
            _ = ReferenceRecording.from_hdf5(reference, legacy=legacy)
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise ValueError('An error occurred while trying to read the reference recording file. '
                            'Make sure it conforms to the OMEGAFormat reference recording format. '
                            'If you are sure it does, please file an issue.') from e
        else: 
            typer.echo(typer.style(f'The OMEGAFormat reference file {reference} conforms to the specification and passes basic sanity checks.', fg=typer.colors.GREEN, bold=True))


    if perception is not None:
        try:
            _ = PerceptionRecording.from_hdf5(perception, legacy=legacy)
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise ValueError('An error occurred while trying to read the perception recording file. '
                             'Make sure it conforms to the OMEGAFormat perception recording format. '
                             'If you are sure it does, please file an issue.') from e
        else: 
            typer.echo(typer.style(f'The OMEGAFormat perception file {reference} conforms to the specification and passes basic sanity checks.', fg=typer.colors.GREEN, bold=True))


@app.command("version")
def version():
    """
        Returns the version of the OMEGAFormat
    """
    import omega_format
    print(omega_format.__version__)
    return omega_format.__version__


@app.command('generate_json', help='Generate .h and .json from python enums.')
def _generate_enums():
    generate_enums()


app.registered_commands = app.registered_commands + convert_odr_app.registered_commands + levelx_app.registered_commands
if __name__ == "__main__":
    app()
