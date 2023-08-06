from __future__ import annotations
from typing import Any
from functools import wraps


class curried:
    """Creates the facade of a curried function

    Creates the facade of a curried function by keeping track of given arguments and calling f only after the required amount is reached

    Attributes:
        f: the function to curry.
        given_args: the arguments currently given to the function
    """
    
    def __init__(self, f: function) -> None:
        """Inits curried with f and with given_args as an empty list

        Args:
            f: The function to curry

        Raises:
            ValueError: a function with keyword only arguments was given
        """
        self.f: function = f
        if f.__code__.co_kwonlyargcount > 0:
            # TODO: add support for functions with keyword only arguments
            raise ValueError("only functions without keyword only arguments can be curried")
        self.given_args = []

    def __call__(self, *args: Any) -> Any:
        """Handles curried calls

        Args:
            *args: Every argument

        Returns:
            If the length of given arguments
                is the amount of arguments required by f,
                The result of the function.
            Otherwise a partially applied version of the curried function.
            
            For example:
                def add(a, b):
                    return a + b

                c_add = curried(add)
                c_add(1) # returns a new partially applied curried
                c_add(1, 2) # returns 3

        Raises:
            TypeError: the length of the length of given arguments exceeds the amount of arguments needed by the curried function
        """

        ga = [*self.given_args, *args]
        if len(ga) == self.f.__code__.co_argcount:
            return self.f(*ga)
        elif len(ga) > self.f.__code__.co_argcount:
            raise TypeError(f"{self.f.__code__.co_name}() takes {self.f.__code__.co_argcount} positional arguments but {len(ga)} were given")
        ret = curried(self.f)
        ret.given_args = ga
        return ret

    def uncurry(self) -> function:
        """Uncurries function by returning the underlying function"""
        return self.f

    def reset(self):
        """Removes partial application by removing all previously applied arguments."""
        self.given_args = []


def curry(f):
    """A decorator to create a function which returns a curried version of the decorated function every call."""
    @wraps(f)
    def decorated(*args):
        return curried(f)(*args)
    return decorated

