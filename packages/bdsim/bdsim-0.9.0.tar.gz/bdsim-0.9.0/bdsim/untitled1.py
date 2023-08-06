#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 08:29:37 2020

@author: corkep
"""

import numpy as np

# class Struct:
    
#     def __init__(self):
#         self.__dict__['_dict'] = {}
    
#     def __setitem__(self, name, value):
#         self.__dict__['_dict'][name] = value
        
#     def __setattr__(self, name, value):
#         self.__dict__['_dict'][name] = value
        
#     def __getattr__(self, name):
#         return self.__dict__['_dict'][name]
        
#     def __str__(self):
#         return str(self._dict)
    
#     def __repr__(self):
#         def fmt(k, v):
#             if isinstance(v, np.ndarray):
#                 return '{:8s}: {:12s}'.format(k, type(v).__name__ + ' ' + str(v.shape)) 
#             else:
#                 return '{:8s}: {:12s}'.format(k, type(v).__name__)
#         return '\n'.join([fmt(k,v) for k, v in self._dict.items()])
        

# a = Struct()

# a['bob'] = 3
# a['nancy'] = 4
# a.boris = 5
# print(a)

from collections import UserDict

class Struct(UserDict):
    
    def __init__(self, name='Struct'):
        super().__init__()
        self.name = name

    def __setattr__(self, name, value):
        if name in ['data', 'name']:
            super().__setattr__(name, value)
        else:
            self.data[name] = value
        
    def __getattr__(self, name):
        return self.data[name]
        
    def __str__(self):
        return self.name + ' ' + str({k:v for k, v in self.data.items() if not k.startswith('_')})
    
    def __repr__(self):
        def fmt(k, v):
            if isinstance(v, np.ndarray):
                return '{:8s}| {:12s}'.format(k, type(v).__name__ + ' ' + str(v.shape)) 
            else:
                return '{:8s}| {:12s}'.format(k, type(v).__name__)
        return self.name + ':\n' + '\n'.join([fmt(k,v) for k, v in self.data.items() if not k.startswith('_')])
    
a = Struct()

a['bob'] = 3
a['nancy'] = 4
a.boris = 5
print(a)