'''
Common utilities
'''
from enum import Enum


class ChoiceEnum(Enum):
    '''
    Enum with choices attribute for use in models
    '''
    @classmethod
    def choices(cls):
        '''Return choices usable in model fields'''
        return tuple((choice.name, choice.value) for choice in cls)
