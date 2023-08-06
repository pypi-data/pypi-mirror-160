from collections import namedtuple
import toga
from toga.constants import COLUMN, ROW
from toga.sources import Source
import numpy as np
INDEX_KEY="Index"

class FrameData(Source):

    def __init__(self, raw):
        super().__init__()
        self.raw = raw
        self.columns = [c.lower() for c in raw.columns]
        self.struct = namedtuple("row", [INDEX_KEY]+self.columns)
        self.data = [self.struct(*r) for r in self.raw.itertuples()]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        print('__getitem__', index)
        return self.data[index]

    def index(self, entry):
        print(INDEX_KEY, entry)
        return self.data.index(entry)
