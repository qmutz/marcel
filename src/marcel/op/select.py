"""C{select FUNCTION}

C{FUNCTION} is applied to input elements. Elements for which C{FUNCTION}
evaluates to true are emitted as output..
"""

import marcel.core


def select():
    return Select()


class SelectArgParser(marcel.core.ArgParser):

    def __init__(self):
        super().__init__('select')
        self.add_argument('function')


class Select(marcel.core.Op):

    argparser = SelectArgParser()

    def __init__(self):
        super().__init__()
        self.function = None

    def __repr__(self):
        return f'select({self.function})'

    # BaseOp
    
    def doc(self):
        return __doc__

    def setup_1(self):
        self.function = marcel.function.Function(self.function, self.global_state().env.globals())
        self.function.set_op(self)

    def receive(self, x):
        if self.function(*x):
            self.send(x)

    # Op

    def arg_parser(self):
        return Select.argparser
