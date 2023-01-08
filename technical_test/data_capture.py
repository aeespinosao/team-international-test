from __future__ import annotations

class DataCapture():
    
    def __init__(self) -> None:
        self.numbers_count = {}
        self.numbers_stats = {}
        self.has_numbers = False
        self.has_stats = False
    
    def add(self, value: int) -> None:
        pass
    
    def build_stats(self) -> DataCapture:
        return self
    
    def less(self, upper_limit: int) -> int:
        pass
    
    def between(self, lower_limit: int, upper_limit: int) -> int:
        pass
    
    def greater(self, lower_limit: int) -> int:
        pass