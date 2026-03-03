from dataclasses import dataclass
from lstore.index import Index
from collections import defaultdict
from time import time

INDIRECTION_COLUMN = 0
RID_COLUMN = 1
TIMESTAMP_COLUMN = 2
SCHEMA_ENCODING_COLUMN = 3

@dataclass
class RID:
    page_range: int
    column_no: int
    page_number: int
    offset: int

class Record:

    def __init__(self, rid, key, columns):
        self.rid = rid
        self.key = key
        self.columns = columns

class Table:

    """
    :param name: string         #Table name
    :param num_columns: int     #Number of Columns: all columns are integer
    :param key: int             #Index of table key in columns
    """
    def __init__(self, name, num_columns, key):
        self.name = name
        self.key = key
        self.num_columns = num_columns

        self.base_page_directory = defaultdict(lambda: [str for _ in range(num_columns)])
        self.tail_page_directory = defaultdict(lambda: [str for _ in range(num_columns)])

        self.index = Index(self)
        self.merge_threshold_pages = 50  # The threshold to trigger a merge

    def __merge(self):
        print("merge is happening")
 
