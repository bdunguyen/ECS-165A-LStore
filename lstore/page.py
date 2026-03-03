SLOT_SIZE = 8

class Page:

    def __init__(self):
        self.num_records = 0
        self.length = SLOT_SIZE
        self.data = bytearray(4096)
        self.cur = 0

    def has_capacity(self):
        space = len(self.data)
        
        if space >= self.curr + self.length:
            return True
        else: 
            return False

    def read(self, offset):
        byte_value = self.data[offset * self.length: offset * self.length + 5]
        return int.from_bytes(byte_value, "big", signed=True)

    def write(self, value, offset = None):
        if offset is None:
            self.location = self.curr
        else:
            self.location = offset * self.length
        if self.has_capacity(value):
            self.data[self.location: self.location + self.length] = value.to_bytes(self.length, "big", signed=True)
            # update curr to track the highest offset written
            if self.location + self.length > self.curr:
                self.curr = self.location + self.length
                self.num_records += 1
            return True
        return False

