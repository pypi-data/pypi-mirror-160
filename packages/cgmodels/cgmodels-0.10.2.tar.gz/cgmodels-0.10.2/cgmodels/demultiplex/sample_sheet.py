import logging
from copy import deepcopy
from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, Field, parse_obj_as
from typing_extensions import Literal

from cgmodels.exceptions import SampleSheetError

SAMPLE_SHEET_HEADER = [
    "FCID",
    "Lane",
    "SampleID",
    "SampleRef",
    "index",
    "SampleName",
    "Control",
    "Recipe",
    "Operator",
    "Project",
]

NOVASEQ_HEADER = deepcopy(SAMPLE_SHEET_HEADER)
NOVASEQ_HEADER.extend("index2")

# This is a map from the headers to the keys to simplify creation of sample sheets
HEADER_MAP = {
    "FCID": "flow_cell",
    "Lane": "lane",
    "SampleID": "sample_id",
    "SampleRef": "reference",
    "index": "index",
    "index2": "second_index",
    "SampleName": "sample_name",
    "Control": "control",
    "Recipe": "recipe",
    "Operator": "operator",
    "Project": "project",
}
LOG = logging.getLogger(__name__)


class BaseSample(BaseModel):
    """This model is used when creating sample sheets"""

    flow_cell: str
    lane: int
    sample_id: str
    reference: str
    index: str
    second_index: str = None
    sample_name: str
    control: str
    recipe: str
    operator: str
    project: str


class Sample(BaseModel):
    """This model is used when parsing/validating existing sample sheets"""

    flow_cell: str = Field(..., alias="FCID")
    lane: int = Field(..., alias="Lane")
    sample_id: str = Field(..., alias="SampleID")
    reference: str = Field(..., alias="SampleRef")
    index: str = Field(..., alias="index")
    sample_name: str = Field(..., alias="SampleName")
    control: str = Field(..., alias="Control")
    recipe: str = Field(..., alias="Recipe")
    operator: str = Field(..., alias="Operator")
    project: str = Field(..., alias="Project")


class NovaSeqSample(Sample):
    """This model is used when parsing/validating existing novaseq sample sheets"""

    second_index: str = Field(..., alias="index2")


class NovaSeqSampleBcl2Fastq(NovaSeqSample):
    sample_id: str = Field(..., alias="SampleID")
    project: str = Field(..., alias="Project")


class NovaSeqSampleDragen(NovaSeqSample):
    sample_id: str = Field(..., alias="Sample_ID")
    project: str = Field(..., alias="Sample_Project")


class SampleSheet(BaseModel):
    type: str
    samples: List[Sample]


class SampleSheetBcl2Fastq(SampleSheet):
    samples: List[NovaSeqSampleBcl2Fastq]


class SampleSheetDragen(SampleSheet):
    samples: List[NovaSeqSampleDragen]


def validate_unique_sample(samples: List[Sample]) -> None:
    """Validate that each sample only exists once"""
    sample_ids: set = set()
    for sample in samples:
        sample_id: str = sample.sample_id.split("_")[0]
        if sample_id in sample_ids:
            message: str = f"Sample {sample.sample_id} exists multiple times in sample sheet"
            LOG.warning(message)
            raise SampleSheetError(message)
        sample_ids.add(sample_id)


def samples_by_lane(samples: List[Sample]) -> Dict[int, List[Sample]]:
    """Group samples by lane"""
    LOG.info("Order samples by lane")
    sample_by_lane: Dict[int, List[Sample]] = {}
    for sample in samples:
        if sample.lane not in sample_by_lane:
            sample_by_lane[sample.lane] = []
        sample_by_lane[sample.lane].append(sample)
    return sample_by_lane


def validate_samples_unique_per_lane(samples: List[Sample]) -> None:
    """Validate that each sample only exists once per lane in a sample sheet"""

    sample_by_lane: Dict[int, List[Sample]] = samples_by_lane(samples)
    for lane, lane_samples in sample_by_lane.items():
        LOG.info("Validate that samples are unique in lane %s", lane)
        validate_unique_sample(lane_samples)


def get_raw_samples(sample_sheet: str) -> List[Dict[str, str]]:
    sample_sheet_rows: List[str] = sample_sheet.split("\n")
    header: List[str] = []
    raw_samples: List[Dict[str, str]] = []
    for line in sample_sheet_rows:
        # Skip empty lines
        if not len(line) > 5:
            continue
        # Check if we are on the header row
        line = line.strip()
        if line.startswith("FCID"):
            header = line.split(",")
            continue
        # Skip rows until header is found
        if not header:
            continue
        raw_samples.append(dict(zip(header, line.split(","))))
    if not header:
        message = "Could not find header in sample sheet"
        LOG.warning(message)
        raise SampleSheetError(message)
    if not raw_samples:
        message = "Could not find any samples in sample sheet"
        LOG.warning(message)
        raise SampleSheetError(message)
    return raw_samples


def get_sample_sheet(
    sample_sheet: str, sheet_type: Literal["2500", "SP", "S2", "S4"], bcl_converter: str
) -> SampleSheet:
    """Parse and validate a sample sheet

    return the information as a SampleSheet object
    """
    # Skip the [data] header
    novaseqsample = {"bcl2fastq": NovaSeqSampleBcl2Fastq, "dragen": NovaSeqSampleDragen}
    raw_samples: List[Dict[str, str]] = get_raw_samples(sample_sheet)
    sample_type = Sample if sheet_type == "2500" else novaseqsample[bcl_converter]
    samples = parse_obj_as(List[sample_type], raw_samples)
    validate_samples_unique_per_lane(samples)
    return SampleSheet(type=sheet_type, samples=samples)


def get_sample_sheet_from_file(
    infile: Path, sheet_type: Literal["2500", "SP", "S2", "S4"], bcl_converter: str
) -> SampleSheet:
    """Parse and validate a sample sheet from file"""
    with open(infile, "r") as csv_file:
        # Skip the [data] header
        sample_sheet: SampleSheet = get_sample_sheet(
            sample_sheet=csv_file.read(), sheet_type=sheet_type, bcl_converter=bcl_converter
        )

    return sample_sheet
