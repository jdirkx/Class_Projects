"""
Jacob Dirkx 
expr.py - calculator 
2/5/24
"""


ENV: dict[str, "IntConst"] = dict()

def env_clear():
    """Clear all variables in calculator memory"""
    global ENV
    ENV = dict()

class Expr(object):
    """Abstract base class of all expressions."""

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError(
            f"'eval' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define 'eval'")

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        raise NotImplementedError(
            f"'__str__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__str__'")

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        raise NotImplementedError(
            f"'__repr__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__repr__'")
    
    
class IntConst: 

    def __init__(self, value: int) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.value}"
    
    def __repr__(self) -> str:
        return f"IntConst({self.value})"

    def __eq__(self, other):
        return isinstance(other, IntConst) and self.value == other.value

    def eval(self):
        return self

class BinOp(Expr):
    """Abstract base class for binary operations"""

    def __init__(self, left: Expr, right: Expr, symbol: str="?Operation symbol undefined"):
        self.left = left
        self.right = right
        self.symbol = symbol

    def __str__(self) -> str:
        return f"({self.left} {self.symbol} {self.right})"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({repr(self.left)}, {repr(self.right)})"
    
    def _apply(self, left_val: int, right_val: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")
    
    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(self._apply(left_val.value, right_val.value))

class Plus(BinOp):
    """Expr + Expr"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="+")
    
    def _apply(self, left: int, right: int) -> int:
        return left + right
    
class Minus(BinOp):
    """Expr - Expr"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="-")
    
    def _apply(self, left: int, right: int) -> int:
        return left - right
    
class Times(BinOp):
    """Expr * Expr"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="*")

    def _apply(self, left: int, right: int) -> int:
        return left * right

class Div(BinOp):
    """Expr // Expr"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="/")

    def _apply(self, left: int, right: int) -> int:
        return left // right

class Unop:
    "Abstract base class for negation/abs value"
       
    def __init__(self, left: Expr, symbol: str="?Operation symbol undefined"):
        self.left = left
        self.symbol = symbol

    def __str__(self) -> str:
        return f"({self.symbol} {self.left})"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({repr(self.left)})"
    
    def _apply(self, left: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")
    
    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.left.eval()
        return IntConst(self._apply(left_val.value))
    

class Neg(Unop):
    "Expr -> -Expr"
    def __init__(self, left: Expr):
        super().__init__(left, symbol="~")
    
    def _apply(self, left: int) -> int:
        return -left

class Abs(Unop):
    "Expr -> |Expr|"
    def __init__(self, left: Expr):
        super().__init__(left, symbol="@")
    
    def _apply(self, left: int) -> int:
        return abs(left)
    
class UndefinedVariable(Exception):
    """Raised when expression tries to use a variable that 
    is not in ENV
    """
    pass

class Var(Expr):
    "Adds variables to calculator memory"
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var({self.name})"
    
    def assign(self, value: IntConst):
        global ENV
        ENV[self.name] = value

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been assigned a value")
        
class Assign(Expr):
    """Assignment:  x = E represented as Assign(x, E)"""

    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var)  # Can only assign to variables! 
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} = {self.right})"

    def __repr__(self):
        return f"Assign({repr(self.left)}, {repr(self.right)})"

    def eval(self) -> IntConst:
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val
