
from collections import UserDict
import numpy as np

class BDStruct(UserDict):
    """
    A dict-like object that allows items to be added by attribute or by key.
    
    For example::
        
        >>> d = Struct('thing')
        >>> d.a = 1
        >>> d['b'] = 2
        >>> d.a
        1
        >>> d['a']
        1
        >>> d.b
        2
        >>> str(d)
        "thing {'a': 1, 'b': 2}"
    """
    
    def __init__(self, name='BDStruct', **kwargs):
        super().__init__()
        self.name = name
        for key, value in kwargs.items():
            self[key] = value

    def __setattr__(self, name, value):
        # invoked by struct[name] = value
        if name in ['data', 'name']:
            super().__setattr__(name, value)
        else:
            self.data[name] = value
    
    def add(self, name, value):
        self.data[name] = value

    def __getattr__(self, name):
        # return self.data[name]
        # some tricks to make this deepcopy safe
        # https://stackoverflow.com/questions/40583131/python-deepcopy-with-custom-getattr-and-setattr
        # https://stackoverflow.com/questions/25977996/supporting-the-deep-copy-operation-on-a-custom-class
        try:
            return self.data[name]
        except AttributeError:
            raise AttributeError('unknown attribute ' + name)
        
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        rows = []

        if len(self) == 0:
            return ''
        maxwidth = max([len(key) for key in self.keys()])
        # if self.name is not None:
        #     rows.append(self.name + '::')
        for k, v in sorted(self.items(), key=lambda x: x[0]):
            if isinstance(v, BDStruct):
                rows.append("{:s}.{:s}::".format(k.ljust(maxwidth), v.name))
                rows.append('\n'.join([' ' * (maxwidth + 3) + line for line in str(v).split('\n')]))
            elif isinstance(v, str):
                rows.append('{:s} = "{:s}" ({:s})'.format(k.ljust(maxwidth), str(v), type(v).__name__))
            else:
                rows.append("{:s} = {:s} ({:s})".format(k.ljust(maxwidth), str(v), type(v).__name__))

        return '\n'.join(rows)

    # def __str__(self):
    #     def fmt(k, v, indent=0):
    #         if isinstance(v, BDStruct):
    #             s = '{:12s}: {:12s}\n'.format(k, type(v).__name__)
    #             for k, v in v.items():
    #                 s += fmt(k, v, indent + 1)
    #             return s
    #         elif isinstance(v, np.ndarray):
    #             s = '            > ' * indent + '{:12s}| {:s}\n'.format(k, type(v).__name__ + ' ' + str(v.shape))
    #         else:
    #             s = '            > ' * indent + '{:12s}| {:s} = {}\n'.format(k, type(v).__name__, v)
    #         return s

    #     s = ''
    #     for k, v in self.data.items():
    #         if k.startswith('_'):
    #             continue
    #         s += fmt(k, v)

    #     return self.name + ':\n' + s

# class BDStruct(AttrDict):

#     def __str__(self):
#         rows = []

#         if len(self) == 0:
#             return ''
#         maxwidth = max([len(key) for key in self.keys()])
#         if self._name is not None:
#             rows.append(self._name + '::')
#         for k, v in sorted(self.items(), key=lambda x: x[0]):
#             if isinstance(v, BDStruct):
#                 rows.append("{:s} .".format(k.ljust(maxwidth)))
#                 rows.append('\n'.join([' ' * (maxwidth + 3) + line for line in str(v).split('\n')]))
#             elif isinstance(v, str):
#                 rows.append('{:s} = "{:s}" ({:s})'.format(k.ljust(maxwidth), str(v), type(v).__name__))
#             else:
#                 rows.append("{:s} = {:s} ({:s})".format(k.ljust(maxwidth), str(v), type(v).__name__))

#         return '\n'.join(rows)

#     def __repr__(self):
#         return self.__str__()

    # def __init__(self, name=None, **kwargs):
    #     self._name = name
    #     # super().__init__(**kwargs)

x = BDStruct()

x['a'] = 3
print(x['a'])
x.b = 4
print(len(x))
print(x.a)
for k, v in x.items():
    print(k, v)
print(x)
x.z = BDStruct(name='baz', foo=3, bar=4)
print(x.z)
print(x.z.foo)
print(x)

class OptBase():

    def __init__(self, a, d):

        super().__init__()
        self.priority = a.keys()

        self.dict = BDStruct(**{**d, **a})

    def __getattr__(self, name):
        return self.dict[name]

    def set(self, **changes):
        for name, value in changes.items():
            if name not in self.priority:
                self.dict[name] = value

o = OptBase(dict(foo=1, bar='hello'), dict(foo=2, baz=3))
print(o.foo)
o.set(foo = 7)
print(o.foo)

print(o.baz)
o.set(baz = 7)
print(o.baz)
