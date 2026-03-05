from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        self.processed_count: int = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            count = len(data_batch)
            self.processed_count += count
            temp_v: List[float] = []
            for item in data_batch:
                if str(item).startswith("temp:"):
                    value = float(str(item).split(':')[1])
                    temp_v.append(value)
            if temp_v:
                avg_temp = sum(temp_v) / len(temp_v)
                return (f"Sensor analysis: {count} readings processed,"
                        f" avg temp: {avg_temp}°C")
            else:
                return f"Sensor analysis: {count} readings processed"
        except (ValueError, IndexError, ZeroDivisionError) as e:
            return f"Error processing sensor batch: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria is None:
            return data_batch
        return [item for item in data_batch
                if str(item).startswith(criteria)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "type": "Environmental Data",
            "processed": self.processed_count
        }
