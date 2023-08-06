class Composable:
    """
    Implements the pipe operator.
    """

    def __init__(self, callable):
        """
        Creates a composable from a given callable.
        """

        self.callable = callable


    def __call__(self, x):
        """
        Calls the internal callable object.
        """

        return self.callable(x)


    def __or__(self, other):
        """
        Composes this composable with another.
        """

        return Composable(
            lambda x: other.callable(self.callable(x))
        )
