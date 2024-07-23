"""Test for fetch and update metdata annotation."""

import json
from pathlib import (
    Path,
)
from typing import (
    Any,
)

import pytest

from plugins.update_plugin_metadata.fetch_annotation import (
    parse_annotation,
)


@pytest.fixture(name="test_data_dir")
def make_test_data_dir() -> Path:
    """Returns Path to test data directory as pathlib.Path."""
    path = Path(__file__).parents[0] / "test_data/"
    return path


@pytest.fixture(name="email_kili_ann_json_path")
def make_kili_ann_json_path(test_data_dir: Path) -> Path:
    """Returns Path to test kili-e2x annotation json."""
    return test_data_dir.joinpath("email_kili.ann.json")


@pytest.fixture(name="email_kili_ann_json")
def load_kili_ann_json(email_kili_ann_json_path: Path) -> dict[str, Any]:
    """Loads the kili-e2x annotation json."""
    with open(email_kili_ann_json_path, "r") as file:
        email_kili_ann_json: dict[str, Any] = json.load(file)
    return email_kili_ann_json


def test_fetch_annotation_succed(email_kili_ann_json: dict[str, Any]) -> None:
    """Test for fetch annotation."""
    json_response_expected = {
        "organization": "KCD",
        "customer_erp_id": "test-custommer",
        "document_id": "test-document",
    }

    json_response = parse_annotation(email_kili_ann_json)

    assert json_response_expected == json_response
