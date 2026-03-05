from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional, Protocol


class ProcessingStage(Protocol):

    def process(self, data: Any) -> Any:
        pass


class InputStage:

    def process(self, data: Any) -> Dict:
        if data is None or data == "":
            raise ValueError("invalid data")
        if isinstance(data, list):
            print("Input: Real-time sensor stream")
        if isinstance(data, dict):
            print(f'Input: "{data}"')
            return data


class TransformStage:
    def process(self, data: Any) -> Any:
        if isinstance(data, dict):
            print("Transform: Enriched with metadata and validation")
        elif isinstance(data, str):
            print("Transform: Parsed and structured data")
        elif isinstance(data, list):
            print("Transform: Aggregated and filtered")
        return data


class OutputStage:
    def process(self, data: Any) -> Any:
        return data

class ProcessingPipeline(ABC):
    ...
