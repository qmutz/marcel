"""C{sort [KEY]}

Input objects are sorted before being written to output. Ordering is based on the use of comparison operators
for type input objects, except if KEY (a function) is provided. In that case, the comparison operators are applied
to the values obtained by applying the KEY function to the input objects.

KEY                        Obtains the sort key. If omitted, the object itself is used as the sort key.
"""

import sys

import osh.core


def sort():
    return Sort()


class SortArgParser(osh.core.OshArgParser):
    
    def __init__(self):
        super().__init__('sort')
        self.add_argument('key', nargs='?', default=None)
        

class Sort(osh.core.Op):

    argparser = SortArgParser()

    def __init__(self):
        super().__init__()
        self.key = None
        self.contents = []

    def __repr__(self):
        return 'sort'

    # BaseOp
    
    def doc(self):
        return __doc__

    def setup(self):
        pass
    
    def receive(self, x):
        self.contents.append(x)
    
    def receive_complete(self):
        if self.key:
            key = self.source_to_function(self.key)
            self.contents.sort(key=lambda t: key(*t))
        else:
            self.contents.sort()
        for x in self.contents:
            self.send(x)
        self.send_complete()

    # Op

    def arg_parser(self):
        return Sort.argparser
