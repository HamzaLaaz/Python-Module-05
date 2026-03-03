from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        return isinstance(data, list) and all(
            isinstance(x, (int, float)) for x in data)

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid data")
            total = sum(data)
            avg = total / len(data) if len(data) > 0 else 0
            result = (f"Processed {len(data)} numeric values,"
                      f" sum={total}, avg={avg}")
            return result
        except ValueError as e:
            return f"Error: {e}"


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:
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

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) and ":" in data

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid log data")
            parts = data.split(":", 1)
            if len(parts) != 2:
                raise ValueError("Invalid log format")
            level = data.split(":", 1)[0].strip()
            message = data.split(":", 1)[1].strip()
            if level == "ERROR":
                result = f"[ALERT] ERROR level detected: {message}"
                return result
            else:
                result = f"[INFO] {level} level detected: {message}"
                return result
        except ValueError as e:
            return f"Error: {e}"


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    data1 = [1, 2, 3, 4, 5]
    print("Initializing Numeric Processor...")
    print(f"Processing data: {data1}")
    print("Validation: Numeric data verified")
    processor1 = NumericProcessor()
    result1 = processor1.process(data1)
    print(processor1.format_output(result1))
    print()
    data2 = "Hello Nexus World"
    print("Initializing Text Processor...")
    print(f'Processing data: "{data2}"')
    print("Validation: Text data verified")
    processor2 = TextProcessor()
    result2 = processor2.process(data2)
    print(processor2.format_output(result2))
    print()
    data3 = "ERROR: Connection timeout"
    print("Initializing Log Processor...")
    print(f'Processing data: "{data3}"')
    print("Validation: Log entry verified")
    processor3 = LogProcessor()
    result3 = processor3.process(data3)
    print(processor3.format_output(result3))
    print()
    print("=== Polymorphic Processing Demo ===")
    processors = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor(),
    ]
    datas = [
        [1, 2, 3],
        "Hello Nexuss",
        "INFO: System ready",
    ]
    print("Processing multiple data types through same interface...")
    for i, (proc, data) in enumerate(zip(processors, datas), 1):
        result = proc.process(data)
        print(f"Result {i}: {result}")
    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()


# print("Processing multiple data types through same interface...")
# i = 1
# proc = NumericProcessor()
# data = [1, 2, 3]
# result = proc.process(data)
# print(f"Result {i}: {result}")

# i = 2
# proc = TextProcessor()
# data = "Hello Nexuss"
# result = proc.process(data)
# print(f"Result {i}: {result}")

# i = 3
# proc = LogProcessor()
# data = "INFO: System ready"
# result = proc.process(data)
# print(f"Result {i}: {result}")
