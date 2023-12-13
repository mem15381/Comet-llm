# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2023 Comet ML INC
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this package.
# *******************************************************

import json
import pathlib
import tempfile
from typing import Dict, Optional

import comet_ml

from .. import convert
from ..chains import deepmerge
from ..types import JSONEncodable


class LLMTraceAPI:
    _api_experiment: comet_ml.APIExperiment

    def __init__(self) -> None:
        raise NotImplementedError(
            "Please use API.get_llm_trace_by_key or API.get_llm_trace_by_name methods to get the instance"
        )

    @classmethod
    def __api__from_api_experiment__(
        cls, api_experiment: comet_ml.APIExperiment
    ) -> "LLMTraceAPI":
        instance = object.__new__(cls)
        instance._api_experiment = api_experiment

        return instance

    def get_name(self) -> Optional[str]:
        """
        Get the name of the trace
        """
        return self._api_experiment.get_name()  # type: ignore

    def get_key(self) -> str:
        """
        Get the unique identifier for this trace
        """
        return self._api_experiment.key  # type: ignore

    def log_user_feedback(self, score: float) -> None:
        """
        Log user feedback

        Args:
            score: float, the feedback score. Can be either 0, 0.0, 1 or 1.0
        """
        ALLOWED_SCORES = [0.0, 1.0]
        if score not in ALLOWED_SCORES:
            raise ValueError(
                f"Score it not valid, should be {ALLOWED_SCORES} but got {score}"
            )

        self._api_experiment.log_metric("user_feedback", score)

    def _get_trace_data(self) -> Dict[str, JSONEncodable]:
        try:
            asset_id = next(
                x
                for x in self._api_experiment.get_asset_list()
                if x["fileName"] == "comet_llm_data.json"
            )["assetId"]
        except Exception:
            raise ValueError(
                "Failed update metadata for this trace, metadata is not available"
            )

        trace_data = json.loads(self._api_experiment.get_asset(asset_id))

        return trace_data  # type: ignore

    def get_metadata(self) -> Dict[str, JSONEncodable]:
        """
        Get trace metadata
        """
        trace_data = self._get_trace_data()

        return trace_data["metadata"]  # type: ignore

    def update_metadata(self, metadata: Dict[str, JSONEncodable]) -> None:
        """
        Update the metadata field for a trace, can be used to set or update metadata fields

        Args:
            metadata_dict: dict, dict in the form of {"metadata_name": value, ...}. Nested metadata is supported
        """

        # Update metadata
        trace_data = self._get_trace_data()
        updated_trace_metadata = deepmerge.deepmerge(
            trace_data.get("metadata", {}), metadata
        )
        trace_data["metadata"] = updated_trace_metadata

        with tempfile.TemporaryDirectory() as temp_dir:
            trace_asset_path = pathlib.Path(temp_dir) / "comet_llm_data.json"
            with open(trace_asset_path, "w") as f:
                json.dump(trace_data, f)

            self._api_experiment.log_asset(trace_asset_path, overwrite=True)

        # Update parameters for trace
        self._api_experiment.log_parameters(
            convert.chain_metadata_to_flat_parameters(metadata)
        )