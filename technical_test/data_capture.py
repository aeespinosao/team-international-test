from __future__ import annotations
from .decorators import range_limit_validation, type_validation, negative_value_validation, has_values_validation, has_stats_validation
from .constants import LOWER_RANGE_LIMIT, UPPER_RANGE_LIMIT

class DataCapture():
    
    def __init__(self) -> None:
        self.numbers_count = {i:0 for i in range(LOWER_RANGE_LIMIT, UPPER_RANGE_LIMIT + 1)}
        self.numbers_stats = {i:0 for i in range(LOWER_RANGE_LIMIT, UPPER_RANGE_LIMIT + 1)}
        self.has_numbers = False
        self.has_stats = False
        self.total_numbers = 0
    
    @type_validation
    @negative_value_validation
    @range_limit_validation
    def add(self, value: int) -> None:
        self.numbers_count[value] += 1
        self.has_numbers = True
        self.total_numbers += 1
    
    @has_values_validation
    def build_stats(self) -> DataCapture:
        cumulative = 0
        
        for value in range(LOWER_RANGE_LIMIT, UPPER_RANGE_LIMIT + 1):
            cumulative += self.numbers_count.get(value)
            self.numbers_stats[value] = cumulative
            
        self.has_stats = True
        return self
    
    @has_stats_validation
    @type_validation
    @negative_value_validation
    @range_limit_validation
    def less(self, upper_limit: int) -> int:
        if upper_limit == LOWER_RANGE_LIMIT:
            return 0
        
        return self.numbers_stats.get(upper_limit - 1)
    
    @has_stats_validation
    @type_validation
    @negative_value_validation
    @range_limit_validation
    def between(self, lower_limit: int, upper_limit: int) -> int:
        if upper_limit < lower_limit:
            lower_limit, upper_limit = upper_limit, lower_limit
        
        return (
            self.numbers_stats.get(upper_limit) - 
            (
                self.numbers_stats.get(lower_limit) - self.numbers_count.get(lower_limit)
            )
        )
    
    @has_stats_validation
    @type_validation
    @negative_value_validation
    @range_limit_validation
    def greater(self, lower_limit: int) -> int:
        if lower_limit == UPPER_RANGE_LIMIT:
            return 0
        
        return self.total_numbers - self.numbers_stats.get(lower_limit)