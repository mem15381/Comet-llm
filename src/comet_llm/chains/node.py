from typing import Dict, Optional

from .. import convert, datetimes
from ..types import JSONEncodable
from . import state


class ChainNode:
    def __init__(
        self,
        input: JSONEncodable,
        category: str,
        name: Optional[str] = None,
        input_metadata: Dict[str, JSONEncodable] = None,
    ):
        self._input = input
        self._outputs = None
        self._id = "the-id"

        self._category = category
        self._name = name
        self._metadata = input_metadata

        self._timer = datetimes.Timer()

        state.get_global_chain().track_node(self)

    @property
    def id(self):
        return self._id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._timer.stop()

    def set_outputs(
        self,
        outputs: Dict[str, JSONEncodable],
        output_metadata: Optional[Dict[str, JSONEncodable]] = None,
    ) -> None:
        self._outputs = outputs
        self._metadata.update(output_metadata)

    def as_dict(self):
        return convert.call_data_to_dict(
            prompt=self._input,
            outputs=self._outputs,
            id="the-id",
            metadata=self._metadata,
            prompt_template=None,
            prompt_template_variables=None,
            start_timestamp=self._timer.start_timestamp,
            end_timestamp=self._timer.end_timestamp,
            duration=self._timer.duration,
        )
