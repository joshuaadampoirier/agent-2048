import numpy as np


class BaseRepresentation:
    """
    Base class for all representations.

    Notes
    -----
    All representations should specify their all the parameters that can be set 
    at the class level in their __init__ as explicit keyword arguments (no *args 
    or **kwargs).
    """

    @classmethod
    def _get_param_names(cls):
        """
        Get parameter names for the representation
        
        Parameters
        ----------
        None 

        Returns
        -------
        params:     list 
                    List of the class parameters.
        """
        # fetch the constructor 
        init = getattr(cls.__init__, 'Representation Class', cls.__init__)

        if init is object.__init__:
            # no constructor to inspect
            params = []
        else:
            # inspect constructor
            sig = inspect.signature(init)
            parameters = [p for p in sig.parameters.values() 
                          if p.name != 'self' and 
                          p.kind != p.VAR_KEYWORD]

            for p in parameters:
                if p.kind == p.VAR_POSITIONAL:
                    raise RuntimeError(
                        'Agent-2048 representations should always specify '
                        'their parameters in the signature of their __init__. '
                        '{class_} with constructor {signature} does not follow '
                        'this convention.'.format(
                            class_=cls, 
                            signature=sig
                        )
                    )

            # Extract and sort argument names excluding 'self'
            params = sorted([p.name for p in parameters])

        return params

    def get_params(self):
        """
        Get parameters for this representation.

        Parameters
        ----------
        None

        Returns
        -------
        params:     dictionary
                    Dictionary of parameters for this representation and each of 
                    their set values.
        """
        # initialize dictionary
        params = dict()

        # loop through parameters, adding to parameter dictionary
        for key in self._get_param_names():
            params[key] = getattr(self, key)

        return params

    def normalize(self, x):
        """
        Normalize a set of input values. 

        Notes
        -----
        2048 tiles are effectively powers of two. To normalize, we will:
            1)  Apply base-2 logarithm to the inputs (2 becomes 1, 8 becomes 3)
            2)  Apply min-max scaling to the remaining values such that all 
                inputs lie between 0 and 1 inclusive.
        """
        # apply base-2 logarithm to inputs
        xl = np.log2(x)

        # return min-max scaled inputs
        return (x - np.min(x)) / (np.max(x) - np.min(x))
