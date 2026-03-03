from collections import OrderedDict
from lstore.page import Page

class Frame:
    def __init__(self, page: Page, page_id: str):
        self.page = page # Page() object
        self.page_id = page_id # TODO: RID / figure out page_id format, maybe "table_name_page_range_col_page_no" ?
        self.dirty = False
        self.pinCounter = 0

class BufferPool:
    def __init__(self, size: int, path: str):
        self.size = size
        self.path = path
        self.pool = OrderedDict() # holds frames

    '''
    Retreives Page
    look in pool, given page_id. If not there, evict if needed & retrieve from disk.
    '''
    def get(self):
        pass

    '''
    Make sure pin counter is 0 first.
    Logic to check if dirty, and remove / write to disk if needed.
    '''
    def evict(self):
        pass

    def write_to_disk(self):
        pass
    
    '''
    Read from disk and put into page object.
    '''
    def read_from_disk(self):
        pass
    
    '''
    Writes all of the frames that are dirty to disk.
    '''
    def push_all(self):
        for page_id in list(self.pool.keys()):
            AccessedFrame = self.pool[page_id]
            
            if AccessedFrame.dirty:
                self.push(page_id)