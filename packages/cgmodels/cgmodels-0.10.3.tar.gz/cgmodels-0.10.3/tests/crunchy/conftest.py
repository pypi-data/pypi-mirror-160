from typing import Dict, List

import pytest


@pytest.fixture(name="file_info")
def fixture_file_info() -> Dict[str, str]:
    return {
        "path": "hej",
        "file": "first_read",
        "checksum": "123",
        "algorithm": "sha256",
        "updated": "2015-01-01",
    }


@pytest.fixture(name="metadata_info")
def fixture_metadata_info() -> List[Dict[str, str]]:
    """Return a list of files that corresponds to a crunchy metadata file"""
    return [
        {
            "path": "first_read_path",
            "file": "first_read",
            "checksum": "checksum_first_read",
            "algorithm": "sha256",
        },
        {
            "path": "second_read_path",
            "file": "second_read",
            "checksum": "checksum_second_read",
            "algorithm": "sha256",
        },
        {"path": "spring_path", "file": "spring"},
    ]
