from collections import UserDict

class UD():

    def __init__(self):
        self._data = dict()

    def __setattr__(self, name, value):
        # invoked by struct[name] = value
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def __getattr__(self, name):
        # return self.data[name]
        # some tricks to make this deepcopy safe
        # https://stackoverflow.com/questions/40583131/python-deepcopy-with-custom-getattr-and-setattr
        # https://stackoverflow.com/questions/25977996/supporting-the-deep-copy-operation-on-a-custom-class
        try:
            return super().__getattribute__('_data')[name]
        except KeyError:
            raise AttributeError('unknown attribute ' + name)

    def __str__(self):
        rows = []
        maxwidth = max([len(key) for key in self._data.keys()])
        for k, v in self._data.items():
            if isinstance(v, UD):
                rows.append("{:s} .".format(k.ljust(maxwidth)))
                rows.append('\n'.join([' ' * (maxwidth + 3) + line for line in str(v).split('\n')]))
            else:
                rows.append("{:s} = {:s} ({:s})".format(k.ljust(maxwidth), str(v), type(v).__name__))

        return '\n'.join(rows)
        

ud = UD()

ud.a = 2
print(ud.a)
ud.blah = 3
print(ud.blah)
print(ud)
print()
ud.d = UD()
ud.d.a = 10
ud.d.b = UD()
ud.d.b.a = 'hello'
ud.d.b.b = 5.6777
ud.d.c = 1.23
print(ud)