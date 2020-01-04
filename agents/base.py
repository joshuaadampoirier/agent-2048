import pickle 
import datetime 


class BaseAgent:
    """
    Base class for all agents in Agent-2048.

    Notes
    -----
    All agents should specify their all the parameters that can be set at the 
    class level in their __init__ as explicit keyword arguments (no *args or 
    **kwargs).
    """


    @classmethod
    def _get_param_names(cls):
        """
        Get parameter names for the estimator
        
        Parameters
        ----------
        None 

        Returns
        -------
        params:     list 
                    List of the class parameters.
        """
        # fetch the constructor 
        init = getattr(cls.__init__, 'Agent Class', cls.__init__)

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
                        'Agent-2048 agents should always specify their '
                        'parameters in the signature of their __init__. '
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
        Get parameters for this agent.

        Parameters
        ----------
        None

        Returns
        -------
        params:     dictionary
                    Dictionary of parameters for this agent and each of their
                    set values.
        """
        # initialize dictionary
        params = dict()

        # loop through parameters, adding to parameter dictionary
        for key in self._get_param_names():
            params[key] = getattr(self, key)

        return params

    def next_move(self):
        """
        Get the next move to be made by the agent.

        Parameters
        ----------
        None 

        Returns
        -------
        next_move:  unicode literal
                    Next maneuver to be played by the agent encoded as one of 
                    the Selenium webdriver common keys 

        Notes
        -----
        All agents should overload this function with their own instance.
        """
        pass

    def _get_filename(self):
        """
        Proposes a filename. 

        Parameters
        ----------
        None 

        Returns
        -------
        filename    string
                    Proposed filename.

        Notes
        -----
        This method is intended to work in conjunction with the save() method.
        If no filename is given to that method, it reaches out to this method
        to propose an available filename.
        """
        # retrieve the class name (lowest subclass)
        class_name = self.__class__.__name__ 

        # determine the timestamp
        dt = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')

        # build the proposed filename
        filename = "{cls_}_{ts}.pkl".format(
            cls_=class_name, 
            ts=dt
        )

        return filename 

    def save(self, filename=None):
        """
        Save the agent.

        Parameters
        ----------
        filename    string
                    File name for the saved object.

        Returns
        -------
        None
        """
        if filename is None:
            filename = self._get_filename()

        pickle.dump(self, open(filename, 'wb'))