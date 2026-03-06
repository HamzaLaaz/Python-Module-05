from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional, Protocol


class ProcessingStage(Protocol):

    def process(self, data: Any) -> Any:
        pass


class InputStage:
    def process(self, data: Any) -> Dict:
        if data is None or data == "":
            raise ValueError("Input: invalid or empty data")
        elif isinstance(data, list):
            return {"type": "Stream", "data": data}
        elif isinstance(data, str):
            return {"type": "CSV", "data": data}
        elif isinstance(data, dict):
            return {"type": "JSON", "data": data}
        raise ValueError("Input: unsupported data type")


class TransformStage:
    def process(self, data: Any) -> Dict:
        if not isinstance(data, dict) or "data" not in data:
            raise ValueError("Transform: unexpected data format")
        data_type = data["type"]
        actual = data["data"]
        if data_type == "Stream":
            data["count"] = len(actual)
            data["avg"] = sum(actual) / len(actual)
            data["transform"] = "Aggregated and filtered"
        elif data_type == "CSV":
            data["word_count"] = len(actual.split(","))
            data["transform"] = "Parsed and structured data"
        elif data_type == "JSON":
            data["transform"] = "Enriched with metadata and validation"
        return data


class OutputStage:
    def process(self, data: Any) -> str:
        if not isinstance(data, dict):
            return "Output: invalid data"
        data_type = data["type"]
        if data_type == "Stream":
            count = data.get("count", 0)
            avg = data.get("avg", 0.0)
            return f"Output: Stream summary: {count} readings, avg: {avg}°C"
        elif data_type == "CSV":
            count = data.get("word_count", 0)
            return f"Output: User activity logged: {count} actions processed"
        elif data_type == "JSON":
            value = data["data"]["value"]
            return f"Output: Processed temperature reading: {value}°C "
        "(Normal range)"
        return "Output: unknown data type"


class ProcessingPipeline(ABC):

    def __init__(self, pipeline_id: str) -> None:
        self.pipeline_id = pipeline_id
        self.stages: List[Any] = []
        self.stats: Dict[str, Union[str, int, float]] = {
            "pipeline_id": pipeline_id,
            "processed": 0,
            "errors": 0
        }

    def add_stage(self, stage: Any) -> None:
        self.stages.append(stage)

    def run_pipeline(self, data: Any) -> str:
        result: Any = data
        for stage in self.stages:
            result = stage.process(result)
        self.stats["processed"] = int(self.stats["processed"]) + 1
        return result

    @abstractmethod
    def process(self, data: Any) -> str:
        pass
