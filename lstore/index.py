from bplustree import BPlusTree
import os
import pickle 
from lstore.table import INDIRECTION_COLUMN, RID_COLUMN
from lstore.page import Page, SLOT_SIZE
"""
A data strucutre holding indices for various columns of a table. Key column should be indexd by default, other columns can be indexed through this object. Indices are usually B-Trees, but other data structures can be used as well.
"""

FILENAME = 'bplustree.db'

class Index:

    def __init__(self, table):
        # One index for each table. All our empty initially.
        self.indices = [None] *  table.num_columns
        self.table = table
    
    def open_Bplus(self, col_num): 
        try: # open the btrees file, test if it is already open
            path = f'{self.table.name}/index/col{col_num}'
            os.makedirs(path, exist_ok= True)
            self.indices[col_num] = BPlusTree(os.path.join(path, FILENAME))
        except PermissionError: # if file is already open, do nothing
            pass
    """
    # returns the location of all records with the given value on column "column"
    """


    def locate(self, column, value):
        self.open_Bplus(column)

        if value in self.indices[column]:
            return self.indices[column][value]
        else:
            return False


    """
    # Returns the RIDs of all records with values in column "column" between "begin" and "end"
    """

    def locate_range(self, begin, end, column):
        recs = []
        for num in range(begin, end):
            recs.append(self.locate(column, num))
        return recs

    """
    # Create index on specific column
    1. check if self.indices is None
    2. if None, then create the Btree and index all previous records
    3. then fill in or append
    """

    def create_index(self, column_number):
        self.open_Bplus(column_number)
        for page_rg in self.table.b_pages_dir:
            indir_col = page_rg[INDIRECTION_COLUMN] 
            for page_id in indir_col:

                page: Page = self.table.database.bufferpool.get(page_id) # returns a page 
                
                rids = [] # (table_name, pgrg, pg_no, offset)
                for offset in range(page.num_records):

                    rid = page[offset * SLOT_SIZE: (offset + 1) * SLOT_SIZE]
                    rids.append(rid)
                
                for rid in rids:
                    
                    page_id = rid.rsplit('_', 1)[0]
                    page: Page = self.table.database.bufferpool.get(page_id)

                    


                # TODO: edit this
    
    def update_index(self, col_num, prev_ind, curr_ind, curr_rid, insert = True):
        '''
        prev_ind: previous indexing key
        curr_ind: indexing key used for update
        '''
        self.open_Bplus(col_num)

        index = self.indices[col_num] 
        if insert: # run on insert
            if curr_ind in index: # if there is already this index (collision behavior)
                copy = pickle.loads(self.indices[col_num][curr_ind])
                copy.append(curr_rid)
                self.indices[col_num][curr_ind] = pickle.dumps(copy)
            else: # if adding to this index for the first time
                self.indices[col_num][curr_ind] = pickle.dumps([curr_rid])
        else: # run on update
            for i, rid in self.indices[col_num][prev_ind]: # check the index of what that record used to be
                if rid == int.from_bytes(prev_ind, 'big'):
                    move_rid = self.indices[col_num][prev_ind].pop(i) # remove and place into new key
                    if curr_ind not in self.indices[col_num]:
                        self.indices[col_num][curr_ind] = pickle.dumps([move_rid])
                    else:
                        copy = pickle.loads(self.indices[col_num][curr_ind])
                        copy.append(move_rid)
                        self.indices[col_num][curr_ind] = pickle.dumps(copy)



        








    """
    # optional: Drop index of specific column
    """

    def drop_index(self, column_number):
        self.indices[column_number] = None

        path = f'{self.table.name}/index/col{column_number}'
        os.remove(path)

