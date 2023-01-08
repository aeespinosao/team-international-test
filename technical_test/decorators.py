from typing import Callable
from .constants import LOWER_RANGE_LIMIT, UPPER_RANGE_LIMIT
from .exceptions import OutOfRangeException, InvalidTypeException, NegativeValueException, NoValuesException, StatsNotFoundException

def range_limit_validation(func: Callable) -> Callable:
    
    def wrapper(self, *args):
        for param in args:
            if param < LOWER_RANGE_LIMIT or param > UPPER_RANGE_LIMIT:
                raise OutOfRangeException(f'{param} is out of rangen [{LOWER_RANGE_LIMIT}, {UPPER_RANGE_LIMIT}]')
            
        return func(self, *args)
        
    return wrapper
     
        
def type_validation(func: Callable) -> Callable:
    
    def wrapper(self, *args):
        for param in args:
            if not isinstance(param, int):
                raise InvalidTypeException(f'{param} is not integer')
        
        return func(self, *args)
        
    return wrapper
      
            
def negative_value_validation(func: Callable) -> Callable:
    
    def wrapper(self, *args):
        for param in args:
            if param < 0:
                raise NegativeValueException(f'{param} is not positive')
        
        return func(self, *args)
        
    return wrapper


def has_values_validation(func: Callable) -> Callable:
    
    def wrapper(self):
        if self.total_numbers == 0:
            raise NoValuesException(f'need to add values')
        
        return func(self)
        
    return wrapper


def has_stats_validation(func: Callable) -> Callable:
    
    def wrapper(self, *args):
        if not self.has_stats:
            raise StatsNotFoundException(f'need to calculate stats')
        
        return func(self, *args)
        
    return wrapper