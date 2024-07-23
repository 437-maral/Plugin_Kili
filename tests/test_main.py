"""Update_plugin_metadata."""

from typing import (
    Any,
)
from unittest.mock import (
    MagicMock,
)

from plugins.update_plugin_metadata.fetch_annotation import (
    update_annotation_properties,
)
from plugins.update_plugin_metadata.main import (
    PluginHandler,
)


def test_update_succeed() -> None:
    """Test the update_annotation method."""
    # Create a mock Kili client

    asset_id = "123"
    label = {
        "CLASSIFICATION_JOB_0": {"categories": [{"name": "KCD", "confidence": 100}]},
        "TRANSCRIPTION_JOB_2": {"text": "test-custommer"},
        "TRANSCRIPTION_JOB_3": {"text": "test-document"},
    }

    mock_kili = MagicMock(name="Kili")

    update_annotation_properties(mock_kili, asset_id, label)

    mock_kili.update_properties_in_assets.assert_called_once()


def test_on_submit_succeeds(caplog: Any) -> None:
    """Test on_submit won't throw an exception."""

    kili = MagicMock(name="Kili")

    PluginHandler(kili, "project_id").on_submit(
        {"jsonResponse": {}, "id": "test_id"}, "asset_id"
    )

    assert "On submit called" in caplog.text


def test_on_review_succeeds(caplog: Any) -> None:
    """Test on_review won't throw an exception."""
    kili = MagicMock(name="Kili")

    PluginHandler(kili, "project_id").on_review(
        {"jsonResponse": {}, "id": "test_id"}, "asset_id"
    )

    assert "On review called" in caplog.text
