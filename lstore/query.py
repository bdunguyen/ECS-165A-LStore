from lstore.table import Table, Record
from lstore.index import Index
from lstore.table import RID
from lstore.page import Page, NUM_SLOTS

PAGE_RANGE = 1000

class Query:
    """
    # Creates a Query object that can perform different queries on the specified table 
    Queries that fail must return False
    Queries that succeed should return the result or True
    Any query that crashes (due to exceptions) should return False
    """
    def __init__(self, table):
        self.table = table
    
    """
    # internal Method
    # Read a record with specified RID
    # Returns True upon succesful deletion
    # Return False if record doesn't exist or is locked due to 2PL
    """
    def delete(self, primary_key):
        pass
    
    
    """
    # Insert a record with specified columns
    # Return True upon succesful insertion
    # Returns False if insert fails for whatever reason
    """
    def insert(self, *columns):
        schema_encoding = '0' * self.table.num_columns
        pass

    
    """
    # Read matching record with specified search key
    # :param search_key: the value you want to search based on
    # :param search_key_index: the column index you want to search based on
    # :param projected_columns_index: what columns to return. array of 1 or 0 values.
    # Returns a list of Record objects upon success
    # Returns False if record locked by TPL
    # Assume that select will never be called on a key that doesn't exist
    """
    def select(self, search_key, search_key_index, projected_columns_index):
        pass

    
    """
    # Read matching record with specified search key
    # :param search_key: the value you want to search based on
    # :param search_key_index: the column index you want to search based on
    # :param projected_columns_index: what columns to return. array of 1 or 0 values.
    # :param relative_version: the relative version of the record you need to retreive.
    # Returns a list of Record objects upon success
    # Returns False if record locked by TPL
    # Assume that select will never be called on a key that doesn't exist
    """
    def select_version(self, search_key, search_key_index, projected_columns_index, relative_version):
        pass

    
    """
    # Update a record with specified key and columns
    # Returns True if update is succesful
    # Returns False if no records exist with given key or if the target record cannot be accessed due to 2PL locking
    """
    def update(self, primary_key, *columns):
        pass

    
    """
    :param start_range: int         # Start of the key range to aggregate 
    :param end_range: int           # End of the key range to aggregate 
    :param aggregate_columns: int  # Index of desired column to aggregate
    # this function is only called on the primary key.
    # Returns the summation of the given range upon success
    # Returns False if no record exists in the given range
    """
    def sum(self, start_range, end_range, aggregate_column_index):
        pass

    
    """
    :param start_range: int         # Start of the key range to aggregate 
    :param end_range: int           # End of the key range to aggregate 
    :param aggregate_columns: int  # Index of desired column to aggregate
    :param relative_version: the relative version of the record you need to retreive.
    # this function is only called on the primary key.
    # Returns the summation of the given range upon success
    # Returns False if no record exists in the given range
    """
    def sum_version(self, start_range, end_range, aggregate_column_index, relative_version):
        pass

    
    """
    incremenets one column of the record
    this implementation should work if your select and update queries already work
    :param key: the primary of key of the record to increment
    :param column: the column to increment
    # Returns True is increment is successful
    # Returns False if no record matches key or if target record is locked by 2PL.
    """
    def increment(self, key, column):
        r = self.select(key, self.table.key, [1] * self.table.num_columns)[0]
        if r is not False:
            updated_columns = [None] * self.table.num_columns
            updated_columns[column] = r[column] + 1
            u = self.update(key, *updated_columns)
            return u
        return False

    def assignRID(self, type: str, columns) -> RID: # find the next available space to add data for a whole record
        primary_key = columns[self.table.key]
        page_range = primary_key // PAGE_RANGE

        # base or tail page directory
        if type == 'b':
            pgrange_dict = self.table.b_pages_dir[page_range]
        elif type == 't':
            pgrange_dict = self.table.t_pages_dir[page_range]

        for cols in pgrange_dict.keys(): # col1, col2,... for each col in this page range
            # we need to look for the next available space
            pages: list[str] = pgrange_dict[cols] # page list for a col
            pg_no: int = len(pages) - 1

            page_id: str = pages[pg_no]

            page: Page = self.table.database.bufferpool.get(page_id)

            pg_rec_no: int = page.num_records # gives us the number of records at the last page

            if pg_rec_no >= NUM_SLOTS:
                # if we don't have anymore space, we create a new page in that directory
                # but first ! we have to check the length
                # TODO: Handle merge
                if type == 't' and len(pgrange_dict[cols]) % self.table.merge_threshold_pages == 0:
                    self.table._merge(page_range)

                # new page
                new_page = Page()

                pg_no = len(pages) - 1

                # place it into bufferpool
                new_page_id = new_page.create_page_id(self.table.name, page_range, pg_no, cols)
                self.table.database.bufferpool.put(new_page, dirty_bit = True)

                pgrange_dict[cols].append(new_page_id)
        
        rid = RID(page_range, pg_no, pages[pg_no].curr // pages[pg_no].length)
        return rid # return the RID object