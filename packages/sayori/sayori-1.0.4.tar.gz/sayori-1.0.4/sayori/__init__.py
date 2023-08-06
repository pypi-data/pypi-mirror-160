from typing import Any, Callable


class Composable:
    """
    Implements the pipe operator.
    """

    def __init__(self, callable: Callable):
        """
        Creates a composable from a given callable.
        """

        self.callable = callable


    def __call__(self, x: Any) -> Any:
        """
        Calls the internal callable object.
        """

        return self.callable(x)


    def __or__(self, other: Composable) -> Composable:
        """
        Composes this composable with another.
        """

        return Composable(
            lambda x: other.callable(self.callable(x))
        )
