"""Plugin for fetching annotations."""

from functools import (
    reduce,
)
from typing import (
    Any,
    Dict,
    List,
)

from kili.client import (
    Kili,
)


def get_from_dict(data_dict: Dict, map_list: List, default: Any) -> Any:
    """Map metadata."""
    return reduce(lambda data, key: data.get(key, {}), map_list, data_dict) or default


def parse_annotation(label: Dict) -> Dict[str, Any]:
    """Update function for annotation metadata."""

    if label is not None:
        keys_to_keep = [
            "CLASSIFICATION_JOB_0",
            "TRANSCRIPTION_JOB_2",
            "TRANSCRIPTION_JOB_3",
            "TRANSCRIPTION_JOB",
            "TRANSCRIPTION_JOB_0",
        ]

        key_mapping = {
            "CLASSIFICATION_JOB_0": "organization",
            "TRANSCRIPTION_JOB_2": "customer_erp_id",
            "TRANSCRIPTION_JOB_3": "document_id",
            "TRANSCRIPTION_JOB": "customer_erp_id",
            "TRANSCRIPTION_JOB_0": "document_id",
        }

        filtered_data = {
            key: value for key, value in label.items() if key in keys_to_keep
        }

        json_response_dict = {}
        data_mapped = {}

        for key, value in filtered_data.items():
            new_key = key_mapping.get(key, "")
            if new_key:
                data_mapped[new_key] = value

        json_response_dict = {
            "organization": get_from_dict(
                data_mapped, ["organization", "categories"], [{}]
            )[0].get("name", ""),
            "customer_erp_id": get_from_dict(
                data_mapped, ["customer_erp_id", "text"], ""
            ),
            "document_id": get_from_dict(data_mapped, ["document_id", "text"], ""),
        }

    return json_response_dict


def update_annotation_properties(kili: Kili, asset_id: str, label: Dict) -> None:
    """Update function for annotation metadata."""

    json_response_array = parse_annotation(label=label)
    kili.update_properties_in_assets(
        asset_ids=asset_id, json_metadatas=json_response_array
    )
