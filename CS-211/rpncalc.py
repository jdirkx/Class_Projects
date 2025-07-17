"""Reverse Polish calculator.

This RPN calculator creates an expression tree from
the input.  It prints the expression in algebraic
notation and then prints the result of evaluating it.
"""

import lex
from expr import Var
import expr
import io

BINOPS = { lex.TokenCat.PLUS : expr.Plus,
           lex.TokenCat.TIMES: expr.Times,
           lex.TokenCat.DIV: expr.Div,
           lex.TokenCat.MINUS:  expr.Minus
        }


def calc(text: str):
    """Read and evaluate a single line formula."""
    try:
        result = rpn_parse(text)
        if isinstance(result, list):
            # If it's a list of expressions, evaluate and print each of them
            for exp in result:
                print(f"{exp} => {exp.eval()}")
        else:
            # If it's a single assignment, print the result
            print(f"{result} => {result.eval()}")
    except Exception as e:
        print(e)

def rpn_calc():
    txt = input("Expression (return to quit):")
    while len(txt.strip()) > 0:
        calc(txt)
        txt = input("Expression (return to quit):")
    print("Bye! Thanks for the math!")

def rpn_parse(text: str):
    """Parse text in reverse Polish notation
    into a list of expressions (exactly one if
    the expression is balanced).
    Example:
        rpn_parse("5 3 + 4 * 7")
          => [ Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))),
               IntConst(7) ]
    May raise:  ValueError for lexical or syntactic error in input 
    """
    try:
        tokens = lex.TokenStream(io.StringIO(text))
        stack = []
        while tokens.has_more():
            tok = tokens.take()
            if tok.kind == lex.TokenCat.INT:
                stack.append(expr.IntConst(int(tok.value)))
            elif tok.kind in BINOPS:
                binop_class = BINOPS[tok.kind]
                right = stack.pop()
                left = stack.pop()
                stack.append(binop_class(left, right))
            elif tok.kind == lex.TokenCat.ASSIGN:
                # Check if the next token is a variable or an operator
                next_token = tokens.peek()
                if next_token.kind == lex.TokenCat.VAR:
                    # Extract variable name after the assignment token
                    var_name_token = tokens.take()
                    var_name = var_name_token.value
                    right = stack.pop()  # Value to be assigned
                    return expr.Assign(Var(var_name), right)
                else:
                    # If the next token is an operator, assume assignment is complete
                    right = stack.pop()
                    stack.append(right)

        print("Stack:", stack)
        return stack

    except lex.LexicalError as e:
        raise ValueError(f"Lexical error {e}")
    except IndexError:
        raise ValueError(f"Imbalanced RPN expression, missing operand at {tok.value}")

if __name__ == "__main__":
    """RPN Calculator as main program"""
    rpn_calc()






