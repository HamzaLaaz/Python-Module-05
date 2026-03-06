from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):
    """Abstract base class for all data processors."""
    @abstractmethod
    def process(self, data: Any) -> str:
        """Process the data and return result string."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate if data is appropriate for this processor."""
        pass

    def format_output(self, result: str) -> str:
        """Format the output string."""
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    """Processor specialized for numeric list data."""
    def validate(self, data: Any) -> bool:
        """Validate that data is a non-empty list of numbers."""
        return isinstance(data, list) and len(data) > 0 and all(
            isinstance(x, (int, float)) for x in data)

    def process(self, data: Any) -> str:
        """Process numeric list: compute sum and average."""
        try:
            if not self.validate(data):
                raise ValueError("Invalid data")
            total = sum(data)
            avg = total / len(data)
            result = (f"Processed {len(data)} numeric values,"
                      f" sum={total}, avg={avg}")
            return result
        except ValueError as e:
            return f"Error: {e}"


class TextProcessor(DataProcessor):
    """Processor specialized for text string data."""
    def validate(self, data: Any) -> bool:
        """Validate that data is a non-empty string."""
        return isinstance(data, str)

    def process(self, data: Any) -> str:
        """Process text: count characters and words."""
        try:
            if not self.validate(data):
                raise ValueError("Invalid data")
            count_char = len(data)
            count_word = len(data.split())
            result = (f"Processed text: {count_char} "
                      f"characters, {count_word} words")
            return result
        except ValueError as e:
            return f"Error: {e}"


class LogProcessor(DataProcessor):
    """Processor specialized for log entry strings."""
    def validate(self, data: Any) -> bool:
        """Validate that data is a string containing a colon."""
        return isinstance(data, str) and ":" in data

    def process(self, data: Any) -> str:
        """Process log entry: extract level and message."""
        try:
            if not self.validate(data):
                raise ValueError("Invalid log data")
            parts = data.split(":", 1)
            level = parts[0].strip()
            message = parts[1].strip()
            if level == "ERROR":
                return f"[ALERT] ERROR level detected: {message}"
            return f"[INFO] {level} level detected: {message}"
        except ValueError as e:
            return f"Error: {e}"


def main() -> None:
    """Main function demonstrating polymorphic data processing."""
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    data1: List[int] = [1, 2, 3, 4, 5]
    print("Initializing Numeric Processor...")
    print(f"Processing data: {data1}")
    print("Validation: Numeric data verified")
    processor1: DataProcessor = NumericProcessor()
    result1 = processor1.process(data1)
    print(processor1.format_output(result1))
    print()
    data2: str = "Hello Nexus World"
    print("Initializing Text Processor...")
    print(f'Processing data: "{data2}"')
    print("Validation: Text data verified")
    processor2: DataProcessor = TextProcessor()
    result2 = processor2.process(data2)
    print(processor2.format_output(result2))
    print()
    data3: str = "ERROR: Connection timeout"
    print("Initializing Log Processor...")
    print(f'Processing data: "{data3}"')
    print("Validation: Log entry verified")
    processor3: DataProcessor = LogProcessor()
    result3 = processor3.process(data3)
    print(processor3.format_output(result3))
    print()
    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    proc: DataProcessor = NumericProcessor()
    data: List[int] = [1, 2, 3]
    result = proc.process(data)
    print(f"Result 1: {result}")
    proc: DataProcessor = TextProcessor()
    data: str = "Hello Nexuss"
    result = proc.process(data)
    print(f"Result 2: {result}")
    proc: DataProcessor = LogProcessor()
    data: str = "INFO: System ready"
    result = proc.process(data)
    print(f"Result 3: {result}")
    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
