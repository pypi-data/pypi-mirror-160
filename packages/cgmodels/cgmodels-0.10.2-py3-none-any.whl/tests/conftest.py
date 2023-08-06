from pathlib import Path

import pytest


@pytest.fixture(name="fixtures")
def fixture_fixtures() -> Path:
    """Return the path to the fixtures directory"""
    return Path("tests/fixtures")


@pytest.fixture(name="hiseq_sample_sheet")
def fixture_hiseq_sample_sheet(fixtures: Path) -> Path:
    """Return the path to a hiseq 2500 sample sheet"""
    return fixtures / "SampleSheet2500.csv"


@pytest.fixture(name="hiseq_dup_sheet")
def fixture_hiseq_dup_sample_sheet(fixtures: Path) -> Path:
    """Return the path to a hiseq 2500 sample sheet with a duplicated sample"""
    return fixtures / "SampleSheet2500_dup.csv"


@pytest.fixture(name="s2_sheet_bcl2fastq")
def fixture_s2_sheet_bcl2fastq(fixtures: Path) -> Path:
    """Return the path to a NovaSeq S2 sample sheet, used in bcl2fastq demultiplexing"""
    return fixtures / "SampleSheetS2_bcl2fastq.csv"


@pytest.fixture(name="s2_sheet_dragen")
def fixture_s2_sheet_dragen(fixtures: Path) -> Path:
    """Return the path to a NovaSeq S2 sample sheet, used in dragen demultiplexing"""
    return fixtures / "SampleSheetS2_dragen.csv"
