from abc import abstractmethod
from enum import Enum


class ProcessFlag(Enum):
    SUCCESS = 1
    CONTAINS_ERRORS = 2
    FAILURE = 3


class Status:
    def __init__(self):
        self.current_flag = ProcessFlag.SUCCESS

    def set_flag(self, val):
        self.current_flag = val


class PreparedData:
    def __init__(self, df):
        self.df = df

    @property
    def corr_matrix(self):
        return self.df.corr()

    @property
    def returns_matrix(self):
        return self.df.pct_change()