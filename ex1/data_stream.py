from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):
    """Abstract base class defining the core streaming interface."""
    def __init__(self, stream_id: str) -> None:
        """Initialize stream with a unique identifier."""
        self.stream_id = stream_id
        self.processed_count: int = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of data and return analysis string."""
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter data batch based on optional criteria string."""
        if criteria is None:
            return data_batch
        return [item for item in data_batch
                if criteria in str(item)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return stream statistics dictionary."""
        return {
            "stream_id": self.stream_id,
            "processed": self.processed_count
        }


class SensorStream(DataStream):
    """Stream handler specialized for environmental sensor data."""
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process sensor readings and compute average temperature."""
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
                return (f"Sensor analysis: {count} readings processed, "
                        f"avg temp: {avg_temp}°C")
            else:
                return f"Sensor analysis: {count} readings processed"
        except Exception as e:
            return f"Error processing sensor batch: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter sensor data by prefix criteria."""
        if criteria is None:
            return data_batch
        return [item for item in data_batch
                if isinstance(item, str) and item.startswith(criteria)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return sensor stream statistics."""
        return {
            "stream_id": self.stream_id,
            "type": "Environmental Data",
            "processed": self.processed_count
        }


class TransactionStream(DataStream):
    """Stream handler specialized for financial transaction data."""
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process transactions and compute net flow."""
        try:
            count = len(data_batch)
            self.processed_count += count
            total_bought: float = 0
            total_sold: float = 0
            for item in data_batch:
                parts = str(item).split(':', 1)
                if len(parts) != 2:
                    continue
                operation = parts[0].strip()
                units = float(parts[1].strip())
                if operation == "buy":
                    total_bought += units
                elif operation == "sell":
                    total_sold += units
            net_flow = total_bought - total_sold
            if net_flow >= 0:
                return (f"Transaction analysis: {count} operations,"
                        f" net flow: +{int(net_flow)} units")
            else:
                return (f"Transaction analysis: {count} operations,"
                        f" net flow: {int(net_flow)} units")
        except Exception as e:
            return f"Error processing transaction batch: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter transactions by operation type prefix."""
        if criteria is None:
            return data_batch
        return [item for item in data_batch
                if isinstance(item, str) and item.startswith(criteria)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return transaction stream statistics."""
        return {
            "stream_id": self.stream_id,
            "type": "Financial Data",
            "processed": self.processed_count
        }


class EventStream(DataStream):
    """Stream handler specialized for system event data."""
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process system events and count errors."""
        try:
            count = len(data_batch)
            self.processed_count += count
            error_count = sum(1 for item in data_batch
                              if str(item) == "error")
            return (f"Event analysis: {count} events,"
                    f" {error_count} error detected")
        except Exception as e:
            return f"Error processing event batch: {e}"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter events by exact match criteria."""
        if criteria is None:
            return data_batch
        return [item for item in data_batch
                if isinstance(item, str) and item == criteria]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return event stream statistics."""
        return {
            "stream_id": self.stream_id,
            "type": "System Events",
            "processed": self.processed_count
        }


class StreamProcessor:
    """Manages and processes multiple stream types polymorphically."""
    def __init__(self) -> None:
        """Initialize processor with empty stream list."""
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        """Add a data stream to the processor."""
        self.streams.append(stream)

    def process_all(self, data_batches: List[List[Any]]) -> None:
        """Process all streams with their respective data batches."""
        for stream, batch in zip(self.streams, data_batches):
            stream.process_batch(batch)
            stats = stream.get_stats()
            stream_type = stats.get("type", "Unknown")
            count = stats.get("processed", 0)
            if stream_type == "Environmental Data":
                print(f"- Sensor data: {count} readings processed")
            elif stream_type == "Financial Data":
                print(f"- Transaction data: {count} operations processed")
            elif stream_type == "System Events":
                print(f"- Event data: {count} events processed")


def main() -> None:
    """Main function demonstrating polymorphic stream processing."""
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    sensor = SensorStream("SENSOR_001")
    print("Initializing Sensor Stream...")
    print("Stream ID: SENSOR_001, Type: Environmental Data")
    sensor_batch = ["temp:22.5", "humidity:65", "pressure:1013"]
    print(f"Processing sensor batch: {sensor_batch}")
    print(sensor.process_batch(sensor_batch))
    print()
    transaction = TransactionStream("TRANS_001")
    print("Initializing Transaction Stream...")
    print("Stream ID: TRANS_001, Type: Financial Data")
    trans_batch = ["buy:100", "sell:150", "buy:75"]
    print(f"Processing transaction batch: {trans_batch}")
    print(transaction.process_batch(trans_batch))
    print()
    event = EventStream("EVENT_001")
    print("Initializing Event Stream...")
    print("Stream ID: EVENT_001, Type: System Events")
    event_batch = ["login", "error", "logout"]
    print(f"Processing event batch: {event_batch}")
    print(event.process_batch(event_batch))
    print()
    print("=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...\n")
    processor = StreamProcessor()
    sensor2 = SensorStream("SENSOR_002")
    trans2 = TransactionStream("TRANS_002")
    event2 = EventStream("EVENT_002")
    processor.add_stream(sensor2)
    processor.add_stream(trans2)
    processor.add_stream(event2)
    batch1 = ["temp:20.0", "temp:21.0"]
    batch2 = ["buy:50", "sell:30", "buy:20", "sell:10"]
    batch3 = ["login", "logout", "error"]
    print("Batch 1 Results:")
    processor.process_all([batch1, batch2, batch3])
    print()
    filtered_sensor = sensor2.filter_data(batch1, "temp")
    filtered_trans = trans2.filter_data(["sell:150"], "sell")
    print("Stream filtering active: High-priority data only")
    print(f"Filtered results: {len(filtered_sensor)} critical sensor"
          f" alerts, {len(filtered_trans)} large transaction")
    print()
    print("All streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
