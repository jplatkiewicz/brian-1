# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.36
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _brianlib
import new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class PySwigIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PySwigIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PySwigIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError, "No constructor defined"
    __repr__ = _swig_repr
    __swig_destroy__ = _brianlib.delete_PySwigIterator
    __del__ = lambda self : None;
    def value(*args): return _brianlib.PySwigIterator_value(*args)
    def incr(*args): return _brianlib.PySwigIterator_incr(*args)
    def decr(*args): return _brianlib.PySwigIterator_decr(*args)
    def distance(*args): return _brianlib.PySwigIterator_distance(*args)
    def equal(*args): return _brianlib.PySwigIterator_equal(*args)
    def copy(*args): return _brianlib.PySwigIterator_copy(*args)
    def next(*args): return _brianlib.PySwigIterator_next(*args)
    def previous(*args): return _brianlib.PySwigIterator_previous(*args)
    def advance(*args): return _brianlib.PySwigIterator_advance(*args)
    def __eq__(*args): return _brianlib.PySwigIterator___eq__(*args)
    def __ne__(*args): return _brianlib.PySwigIterator___ne__(*args)
    def __iadd__(*args): return _brianlib.PySwigIterator___iadd__(*args)
    def __isub__(*args): return _brianlib.PySwigIterator___isub__(*args)
    def __add__(*args): return _brianlib.PySwigIterator___add__(*args)
    def __sub__(*args): return _brianlib.PySwigIterator___sub__(*args)
    def __iter__(self): return self
PySwigIterator_swigregister = _brianlib.PySwigIterator_swigregister
PySwigIterator_swigregister(PySwigIterator)

class DoubleVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DoubleVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DoubleVector, name)
    __repr__ = _swig_repr
    def iterator(*args): return _brianlib.DoubleVector_iterator(*args)
    def __iter__(self): return self.iterator()
    def __nonzero__(*args): return _brianlib.DoubleVector___nonzero__(*args)
    def __len__(*args): return _brianlib.DoubleVector___len__(*args)
    def pop(*args): return _brianlib.DoubleVector_pop(*args)
    def __getslice__(*args): return _brianlib.DoubleVector___getslice__(*args)
    def __setslice__(*args): return _brianlib.DoubleVector___setslice__(*args)
    def __delslice__(*args): return _brianlib.DoubleVector___delslice__(*args)
    def __delitem__(*args): return _brianlib.DoubleVector___delitem__(*args)
    def __getitem__(*args): return _brianlib.DoubleVector___getitem__(*args)
    def __setitem__(*args): return _brianlib.DoubleVector___setitem__(*args)
    def append(*args): return _brianlib.DoubleVector_append(*args)
    def empty(*args): return _brianlib.DoubleVector_empty(*args)
    def size(*args): return _brianlib.DoubleVector_size(*args)
    def clear(*args): return _brianlib.DoubleVector_clear(*args)
    def swap(*args): return _brianlib.DoubleVector_swap(*args)
    def get_allocator(*args): return _brianlib.DoubleVector_get_allocator(*args)
    def begin(*args): return _brianlib.DoubleVector_begin(*args)
    def end(*args): return _brianlib.DoubleVector_end(*args)
    def rbegin(*args): return _brianlib.DoubleVector_rbegin(*args)
    def rend(*args): return _brianlib.DoubleVector_rend(*args)
    def pop_back(*args): return _brianlib.DoubleVector_pop_back(*args)
    def erase(*args): return _brianlib.DoubleVector_erase(*args)
    def __init__(self, *args): 
        this = _brianlib.new_DoubleVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(*args): return _brianlib.DoubleVector_push_back(*args)
    def front(*args): return _brianlib.DoubleVector_front(*args)
    def back(*args): return _brianlib.DoubleVector_back(*args)
    def assign(*args): return _brianlib.DoubleVector_assign(*args)
    def resize(*args): return _brianlib.DoubleVector_resize(*args)
    def insert(*args): return _brianlib.DoubleVector_insert(*args)
    def reserve(*args): return _brianlib.DoubleVector_reserve(*args)
    def capacity(*args): return _brianlib.DoubleVector_capacity(*args)
    __swig_destroy__ = _brianlib.delete_DoubleVector
    __del__ = lambda self : None;
DoubleVector_swigregister = _brianlib.DoubleVector_swigregister
DoubleVector_swigregister(DoubleVector)

class LabelledArrays(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LabelledArrays, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LabelledArrays, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _brianlib.new_LabelledArrays(*args)
        try: self.this.append(this)
        except: self.this = this
    def get_msg(*args): return _brianlib.LabelledArrays_get_msg(*args)
    __swig_destroy__ = _brianlib.delete_LabelledArrays
    __del__ = lambda self : None;
LabelledArrays_swigregister = _brianlib.LabelledArrays_swigregister
LabelledArrays_swigregister(LabelledArrays)



