from __future__ import annotations
from .decorators import range_limit_validation, type_validation, negative_value_validation, has_values_validation, has_stats_validation
from .constants import LOWER_RANGE_LIMIT, UPPER_RANGE_LIMIT

class DataCapture():
    """
    DataCapture class provide a way to store some numbers for future statistics
    """
    
    def __init__(self) -> None:
        self.numbers_count = {i:0 for i in range(LOWER_RANGE_LIMIT, UPPER_RANGE_LIMIT + 1)}
        self.has_numbers = False
        self.total_numbers = 0
    
    @type_validation
    @negative_value_validation
    @range_limit_validation
    def add(self, value: int) -> None:
        """
        Append a number that would be used for statistics
        
        Params:
            value: integer 
                number between [1, 1000] to be added.
        """
        self.numbers_count[value] += 1
        self.has_numbers = True
        self.total_numbers += 1
        
    @has_values_validation
    def build_stats(self) -> DataStats:
        return DataStats(self.numbers_count, self.total_numbers)


class DataStats:
    """
    DataStats class provide a way to compute some statistics required for some numbers
    """
    
    def __init__(self, numbers_count: dict, total_numbers: int) -> None:
        self.numbers_count = numbers_count
        self.total_numbers = total_numbers
        self.numbers_stats = {i:0 for i in range(LOWER_RANGE_LIMIT, UPPER_RANGE_LIMIT + 1)}
        self.has_stats = False
        self.build_stats()
    
    def build_stats(self) -> DataCapture:
        """
        Compute the statistics based on the added values
        """
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
        """
        Retrieve the quantity of numbers less than upper_limit
        
        Params:
            upper_limit: integer 
                number between [1, 1000] provided as an upper limit for the statistic
        """
        if upper_limit == LOWER_RANGE_LIMIT:
            return 0
        
        return self.numbers_stats.get(upper_limit - 1)
    
    @has_stats_validation
    @type_validation
    @negative_value_validation
    @range_limit_validation
    def between(self, lower_limit: int, upper_limit: int) -> int:
        """
        Retrieve the quantity of numbers between lower_limit and upper_limit
        
        Params:
            lower_limit: integer 
                number between [1, 1000] provided as an lower limit for the statistic
            upper_limit: integer 
                number between [1, 1000] provided as an upper limit for the statistic
        """
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
        """
        Retrieve the quantity of numbers greater than lower_limit
        
        Params:
            lower_limit: integer 
                number between [1, 1000] provided as an lower limit for the statistic
        """
        if lower_limit == UPPER_RANGE_LIMIT:
            return 0
        
        return self.total_numbers - self.numbers_stats.get(lower_limit)