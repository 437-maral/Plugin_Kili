"""Plugin for validating annotations."""

from typing import (
    Any,
    Dict,
)

from kili.plugins import (
    PluginCore,
)

from .fetch_annotation import (
    parse_annotation,
)


class PluginHandler(PluginCore):
    """Custom Plugin."""

    # pylint: disable=unused-argument,no-self-use
    def on_review(self: Any, label: Dict, asset_id: str) -> None:
        """Dedicated handler for Review action."""
        _on_submit_review_action(
            plugin_handler=self, label=label, asset_id=asset_id, flag_submit=False
        )

    # pylint: disable=unused-argument,no-self-use
    def on_submit(self: Any, label: Dict, asset_id: str) -> None:
        """Dedicated handler for Submit action."""
        _on_submit_review_action(
            plugin_handler=self, label=label, asset_id=asset_id, flag_submit=True
        )


def _on_submit_review_action(
    plugin_handler: PluginHandler, label: Dict, asset_id: str, flag_submit: bool
) -> None:
    """Dedicated handler for review action."""
    plugin_handler.logger.info(
        f"On {'submit' if flag_submit else 'review'} called for asset_id '{asset_id}'."
    )

    json_response_array = parse_annotation(label=label)
    plugin_handler.kili.update_properties_in_assets(
        asset_ids=asset_id, json_metadatas=json_response_array
    )
