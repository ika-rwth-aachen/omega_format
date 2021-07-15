from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.resolve()))
import pytest
import h5py
import typer
from omega_format import PerceptionRecording
from omega_format import ReferenceRecording

app = typer.Typer()


@app.command()
def check_read_write_consistency(input_file: Path = typer.Argument(..., dir_okay=False),
                                 output_file: Path = typer.Option('test.hdf5', dir_okay=False, file_okay=True),
                                 test_perception: bool = typer.Option(False)):
    read_recording = PerceptionRecording if test_perception else ReferenceRecording
    # Test reading and writing of 'known good file'
    ref_rec = read_recording.from_hdf5(input_file)
    ref_rec.to_hdf5(output_file)

    # Test reading and writing of created file
    ref_rec2 = read_recording.from_hdf5(output_file)
    ref_rec2.to_hdf5(output_file)

    # compare output_file to input_file
    input_file_components = []
    with h5py.File(input_file, 'r') as f:
        f.visit(lambda x: input_file_components.append(x))

    output_file_components = []
    with h5py.File(output_file, 'r') as f:
        f.visit(lambda x: output_file_components.append(x))

    diff = set(list(input_file_components)).symmetric_difference(set(list(output_file_components)))
    print(f'Difference of {read_recording.__name__}: {diff}')
    assert len(diff) == 0


def test_reference_consistency():
    inf = Path(__file__).parent.absolute()/'reference_rec.hdf5'
    of = Path(__file__).parent.absolute()/'test_ref.hdf5'
    if not inf.exists():
        pytest.skip(f'ReferenceFormat test file {inf.name} does not exist.')
    try:
        check_read_write_consistency(inf, of, test_perception=False)
    finally:
        of.unlink(missing_ok=True)



def test_perception_consistency():
    inf = Path(__file__).parent.absolute()/'perception_rec.hdf5'
    of = Path(__file__).parent.absolute()/'test_perception.hdf5'
    if not inf.exists():
        pytest.skip(f'PerceptionFormat test file {inf.name} does not exist.')
    try:
        check_read_write_consistency(inf, of, test_perception=True)
    finally:
        of.unlink(missing_ok=True)


if __name__ == "__main__":
    app()
