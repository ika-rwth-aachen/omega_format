import h5py
import typer
from typing import Optional
from lxml import etree
from pathlib import Path
from omega_format.converters.from_asam_opendrive.opendriveconverter.logger import logger
from omega_format.converters.from_asam_opendrive.opendriveconverter.converter import convert_opendrive
from omega_format.converters.from_asam_opendrive.opendriveparser.parser import parse_opendrive
from tqdm.auto import tqdm

from omega_format.reference_recording import DictWithProperties, Road

app = typer.Typer()


def opendrive2roads(odr_file: Path, junction_id: Optional[int] = None,
    step_size: Optional[float] = 0.1) -> DictWithProperties[str, Road]:
    with open(odr_file, "r") as f:
        utf8Parser = etree.XMLParser(encoding='utf-8', huge_tree=True)
        try:
            tree = etree.parse(f, parser=utf8Parser)
            xml = tree.getroot()
        except etree.XMLSyntaxError as e:
            if 'Document is empty' not in str(e):
                raise etree.XMLSyntaxError("File invalid!") from e
            else:
                raise etree.XMLSyntaxError("File empty!") from e

    open_drive_structure = parse_opendrive(xml)
    roads = convert_opendrive(open_drive_structure, step_size, junction_id)
    return roads

@app.command("convert-odr", help='Convert ASAM OpenDRIVE to OMEGAFormat')
def from_opendrive(
    input: Path = typer.Option(exists=True, readable=True, dir_okay=True),
    output: Path = typer.Option(),
    junction_id: Optional[int] = None,
    step_size: Optional[float] = 0.1):
    input = Path(input)
    output = Path(output)
    assert input.is_dir()==output.is_dir()
    if input.is_dir():
        inputs = list(input.glob('*.xodr'))
        output.mkdir(exist_ok=True, parents=True)
        outputs = [output/f'{f.stem}.hdf5' for f in inputs]
    else:
        inputs = [input]
        outputs = [output]
    for input, output in tqdm(list(zip(inputs, outputs))):
        Path(output).parent.mkdir(exist_ok=True, parents=True)
        logger.info(f'Converting file {input.name}...')
        with h5py.File(output, 'w') as f:
            opendrive2roads(input, junction_id=junction_id, step_size=step_size).to_hdf5(f)
        
        logger.info(f'Converted file {input.name} to {output.name}')


if __name__ == "__main__":
    app()