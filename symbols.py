# symbols.py

from dataclasses import dataclass, field
from functools import cached_property

GREEK = {
    "alpha",
    "nu",
    "beta",
    "xi",
    "gamma",
    "delta",
    "pi",
    "epsilon",
    "rho",
    "zeta",
    "sigma",
    "eta",
    "tau",
    "theta",
    "upsilon",
    "iota",
    "phi",
    "kappa",
    "chi",
    "lambda",
    "psi",
    "mu",
    "omega",
}

DECORATOR_LATEX = {
    "bar": r"\bar",
    "hat": r"\hat",
    "dot": r"\dot",
    "ddot": r"\ddot",
}


@dataclass(frozen=True)
class Symbol:
    base: str
    decorators: tuple[str, ...] = field(default_factory=tuple)
    subscripts: tuple[str, ...] = field(default_factory=tuple)
    description: str = ""

    @cached_property
    def latex(self) -> str:
        """
        Decorators are applied left-to-right (outermost last).
        Example: ("bar", "hat") → \\bar{\\hat{x}}
        """
        base = f"\\{self.base}" if self.base in GREEK else self.base

        # decorators (apply ONLY to base)
        if self.decorators:
            for dec in self.decorators:
                if dec not in DECORATOR_LATEX:
                    raise ValueError(
                        "Not a valid decorator. "
                        f"Only {list(DECORATOR_LATEX.keys())} allowed"
                    )
                base = f"{DECORATOR_LATEX[dec]}{{{base}}}"

        # subscripts
        if self.subscripts:
            base += f"_{{{','.join(self.subscripts)}}}"

        return base

    def __str__(self) -> str:
        return self.latex

    def __mul__(self, other):
        return SymbolExpr(self) * other

    def __truediv__(self, other):
        return SymbolExpr(self) / other

    def __add__(self, other):
        return SymbolExpr(self) + other

    def __sub__(self, other):
        return SymbolExpr(self) - other


@dataclass(frozen=True)
class Expr:
    def latex(self) -> str:
        raise NotImplementedError

    def __str__(self):
        return self.latex()

    # operators
    def __mul__(self, other):
        return Mul(self, self._to_expr(other))

    def __truediv__(self, other):
        return Div(self, self._to_expr(other))

    def __add__(self, other):
        return Add(self, self._to_expr(other))

    def __sub__(self, other):
        return Sub(self, self._to_expr(other))

    def _to_expr(self, x):
        if isinstance(x, Expr):
            return x
        if isinstance(x, Symbol):
            return SymbolExpr(x)
        if isinstance(x, (int, float)):
            return Number(x)
        raise TypeError(f"Cannot convert {type(x)} to Expr")


@dataclass(frozen=True)
class SymbolExpr(Expr):
    symbol: Symbol

    def latex(self) -> str:
        return self.symbol.latex


@dataclass(frozen=True)
class Number(Expr):
    value: float

    def latex(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr

    def latex(self) -> str:
        return f"{self.left.latex()} + {self.right.latex()}"


@dataclass(frozen=True)
class Sub(Expr):
    left: Expr
    right: Expr

    def latex(self) -> str:
        return f"{self.left.latex()} - {self.right.latex()}"


@dataclass(frozen=True)
class Mul(Expr):
    left: Expr
    right: Expr

    def latex(self) -> str:
        return f"{self.left.latex()}\\,{self.right.latex()}"


@dataclass(frozen=True)
class Div(Expr):
    left: Expr
    right: Expr

    def latex(self) -> str:
        return r"\frac{" + self.left.latex() + "}{" + self.right.latex() + "}"


N_Ed = Symbol(base="N", subscripts=("Ed",))
chi_LT = Symbol(base="chi", decorators=("bar",), subscripts=("LT",))
A = Symbol(base="A")
f_y = Symbol(base="f_y")

expr = N_Ed / (chi_LT * 1.35 * f_y)


print(expr)
