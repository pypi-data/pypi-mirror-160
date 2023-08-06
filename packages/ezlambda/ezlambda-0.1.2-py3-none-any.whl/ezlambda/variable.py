from __future__ import annotations
from typing import Any, Callable

import sys
import math

class VariableOperationMarker:
    pass

class _VariableSuper(object):
    def getName(self):
        return super().__getattribute__("name")
    
    def setName(self, name):
        super().__setattr__("name", name)
    
    def getChild(self):
        return super().__getattribute__("child")
    
    def setChild(self, child):
        super().__setattr__("child", child)
    
    def getTree(self):
        return super().__getattribute__("tree")
    
    def setTree(self, tree):
        super().__setattr__("tree", tree)
    
    def _execute(self, *args, **kwargs):
        tree = super(Variable, self).getTree()
        name = super(Variable, self).getName()
        # print("tree:", tree, sep="\n")
        # print("args:", args, sep="\n")
        # print("kwargs:", kwargs, sep="\n")
        if tree is None:
            return kwargs[name] if name in kwargs else None if len(args) == 0 else args[0] if len(args) == 1 else args
        return tree.evaluate(*args, **kwargs)

class Variable(_VariableSuper):
    def __init__(self, name: str | None = None, child: Variable | None = None, tree: Callable | None = None) -> None:
        super().setName(name)
        super().setChild(child)
        super().setTree(tree)
    
    def __repr__(self) -> str:
        tree = super().getTree()
        if tree is None:
            return super().getName()
        # return f"V{repr(tree)}"
        return repr(tree)

    def __call__(self, *args, **kwargs) -> Variable | Any:
        tree = super().getTree()
        if len(args) == 0 or not isinstance(args[0], VariableOperationMarker):
            return super()._execute(*args, **kwargs)
        args = args[1:]
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, args, "call", lambda f, a, kw: f(*a, **kw), kwargs))
    
    def __getattribute__(self, __name: str) -> Variable:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, __name, "getattr", lambda x, _name: getattr(x, _name)))
    
    def __setattr__(self, __name: str, __value: Any) -> Variable:  # type: ignore # __setattr__ usually returns None, but here it is used to return an action that will set an object's attribute when called
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, __name, "setattr", lambda x, _name, _value: setattr(x, _name, _value), __value))
    
    def __delattr__(self, __name: str) -> Variable:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, __name, "delattr", lambda x, _name: delattr(x, _name)))
    
    def __pos__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "pos", lambda x: +x))
    
    def __neg__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "neg", lambda x: -x))
    
    def __abs__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "abs", lambda x: abs(x)))
    
    def __invert__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "~", lambda x: ~x))
    
    def __round__(self, *args) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, args, "round", lambda x, a: round(x, *a)))
    
    def __floor__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "floor", lambda x: math.floor(x)))
    
    def __ceil__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "ceil", lambda x: math.ceil(x)))
    
    def __trunc__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "trunc", lambda x: math.trunc(x)))
    
    def __add__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "+", lambda x, y: x + y))
    
    def __sub__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "-", lambda x, y: x - y))
    
    def __mul__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "*", lambda x, y: x * y))
    
    def __pow__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "**", lambda x, y: x ** y))
    
    def __div__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "/", lambda x, y: x / y))
    
    def __floordiv__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "//", lambda x, y: x // y))
    
    def __mod__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "%", lambda x, y: x % y))
    
    def __divmod__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "divmod", lambda x, y: divmod(x, y)))
    
    def __lshift__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "<<", lambda x, y: x << y))
    
    def __rshift__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, ">>", lambda x, y: x >> y))
    
    def __and__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "&", lambda x, y: x & y))
    
    def __or__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "|", lambda x, y: x | y))
    
    def __xor__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "^", lambda x, y: x ^ y))
    
    def __radd__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, tree, "+", lambda x, y: x + y))
    
    def __rsub__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, tree, "-", lambda x, y: x - y))
    
    def __rmul__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, tree, "*", lambda x, y: x * y))
    
    def __rpow__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, tree, "**", lambda x, y: x ** y))
    
    def __rdiv__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, tree, "/", lambda x, y: x / y))
    
    def __rfloordiv__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, tree, "//", lambda x, y: x // y))
    
    def __rmod__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, self, "%", lambda x, y: x % y))
    
    def __rdivmod__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, self, "divmod", lambda x, y: divmod(x, y)))
    
    def __rlshift__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, self, "<<", lambda x, y: x << y))
    
    def __rrshift__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, self, ">>", lambda x, y: x >> y))
    
    def __rand__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, self, "&", lambda x, y: x & y))
    
    def __ror__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, self, "|", lambda x, y: x | y))
    
    def __rxor__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(other, self, "^", lambda x, y: x ^ y))
    
    def __iadd__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "+", lambda x, y: x + y))
    
    def __isub__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "-", lambda x, y: x - y))
    
    def __imul__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "*", lambda x, y: x * y))
    
    def __ipow__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "**", lambda x, y: x ** y))
    
    def __idiv__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "/", lambda x, y: x / y))
    
    def __ifloordiv__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "//", lambda x, y: x // y))
    
    def __imod__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "%", lambda x, y: x % y))
    
    def __idivmod__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "divmod", lambda x, y: divmod(x, y)))
    
    def __ilshift__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "<<", lambda x, y: x << y))
    
    def __irshift__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, ">>", lambda x, y: x >> y))
    
    def __iand__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "&", lambda x, y: x & y))
    
    def __ior__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "|", lambda x, y: x | y))
    
    def __ixor__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "^", lambda x, y: x ^ y))
    
    def __eq__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "==", lambda x, y: x == y))
    
    def __ne__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "!=", lambda x, y: x != y))
    
    def __lt__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "<", lambda x, y: x < y))
    
    def __le__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, "<=", lambda x, y: x <= y))
    
    def __gt__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, ">", lambda x, y: x > y))
    
    def __ge__(self, other: Any) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, other, ">=", lambda x, y: x >= y))
    
    def __int__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "int", lambda x: int(x)))
    
    def __float__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "float", lambda x: float(x)))
    
    def __complex__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "complex", lambda x: complex(x)))
    
    def __oct__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "oct", lambda x: oct(x)))
    
    def __hex__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "hex", lambda x: hex(x)))
    
    def __index__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "index", lambda x: int(x)))
    
    def __bytes__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "bytes", lambda x: bytes(x)))
    
    def __str__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "str", lambda x: str(x)))
    
    def __repr__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "repr", lambda x: repr(x)))
    
    def __format__(self, formatStr) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, formatStr, "format", lambda x, fmt: format(x, fmt)))
    
    def __hash__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "hash", lambda x: hash(x)))
    
    def __bool__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "bool", lambda x: bool(x)))
    
    def __dir__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "dir", lambda x: dir(x)))
    
    def __sizeof__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "sizeof", lambda x: sys.getsizeof(x)))
    
    def __len__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "len", lambda x: len(x)))
    
    def __getitem__(self, __key: str) -> Variable:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, __key, "getitem", lambda x, _key: x[_key]))
    
    def __setitem__(self, __key: str, __value: Any) -> Variable:  # type: ignore # __setitem__ usually returns None, but here it is used to return an action that will set an object's itemibute when called
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, __key, "setitem", lambda x, _key, _value: x.__setitem__(_key, _value), __value))
    
    def __delitem__(self, __key: str) -> Variable:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, __key, "delitem", lambda x, _key: x.__delitem__(_key)))
    
    def __iter__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "iter", lambda x: iter(x)))
    
    def __reversed__(self) -> Any:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, None, "reversed", lambda x: reversed(x)))
    
    def __contains__(self, __item) -> Variable:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, __item, "contains", lambda x, _item: x.__contains__(_item)))
    
    def __missing__(self, __key) -> Variable:
        tree = super().getTree()
        if tree is None:
            tree = self
        return Variable(None, self, _VariableExecutionTree(tree, __key, "missing", lambda x, _key: x.__missing__(_key)))

class _VariableExecutionTree:
    def __init__(self, lChild, rChild, op, func, extraChild=None):
        self.lChild = lChild
        self.rChild = rChild
        self.op = op
        self.func = func
        self.extraChild = extraChild
    
    def __repr__(self):
        return f"({repr(self.lChild)} {self.op} {repr(self.rChild)})"
    
    def evaluate(self, *args, **kwargs):
        return self._evaluate(list(args), kwargs)
    
    def _evaluate(self, args, kwargs):
        if isinstance(self.lChild, _VariableExecutionTree):
            lValue = self.lChild._evaluate(args, kwargs)
        elif isinstance(self.lChild, Variable) and (tree := super(Variable, self.lChild).getTree()) is not None:
            lValue = tree._evaluate(args, kwargs)
        elif isinstance(self.lChild, Variable) and (name := super(Variable, self.lChild).getName()) is not None:
            if name in kwargs:
                lValue = kwargs[name]
            elif len(args) > 0:
                lValue = args.pop(0)
                kwargs[name] = lValue
            else:
                lValue = None
        else:
            lValue = self.lChild
        
        if isinstance(self.rChild, _VariableExecutionTree):
            rValue = self.rChild._evaluate(args, kwargs)
        elif isinstance(self.rChild, Variable) and (tree := super(Variable, self.rChild).getTree()) is not None:
            rValue = tree._evaluate(args, kwargs)
        elif isinstance(self.rChild, Variable) and (name := super(Variable, self.rChild).getName()) is not None:
            if name in kwargs:
                rValue = kwargs[name]
            elif len(args) > 0:
                rValue = args.pop(0)
                kwargs[name] = rValue
            else:
                rValue = None
        else:
            rValue = self.rChild
        
        if isinstance(self.extraChild, _VariableExecutionTree):
            extraValue = self.extraChild._evaluate(args, kwargs)
        elif isinstance(self.extraChild, Variable) and (tree := super(Variable, self.extraChild).getTree()) is not None:
            extraValue = tree._evaluate(args, kwargs)
        elif isinstance(self.extraChild, Variable) and (name := super(Variable, self.extraChild).getName()) is not None:
            if name in kwargs:
                extraValue = kwargs[name]
            elif len(args) > 0:
                extraValue = args.pop(0)
                kwargs[name] = extraValue
            else:
                extraValue = None
        else:
            extraValue = self.extraChild
        
        if self.func is not None:
            if self.extraChild is not None:
                res = self.func(lValue, rValue, extraValue)
            elif self.rChild is not None:
                res = self.func(lValue, rValue)
            else:
                res = self.func(lValue)
        else:
            res = lValue

        return res
