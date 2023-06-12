class Time:
    def __init__(self, value: int = None, unit: str = None) -> None:
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        if self.value is None or self.unit is None:
            raise ValueError("Time value or unit is not set.")
        return f"{self.value}{self.unit}"

    def set_value_and_unit(self, value: int, unit: str) -> None:
        self.value = value
        self.unit = unit
