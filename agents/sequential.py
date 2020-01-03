from agents.base import BaseAgent
from selenium.webdriver.common.keys import Keys 


class SequentialAgent(BaseAgent):
    """
    Class object for the sequential agent.

    This agent is governed by simple logic. Given a starting maneuver (down,
    left, up, right) and a direction (clockwise/counterclockwise) the agent
    sequentially makes those maneuvers.

    Parameters
    ----------
    initial_move:   unicode literal, default 0 (move_up)
                    First move to be made by the agent in the game.

    clockwise:      bool, default True
                    If true, loop through the maneuvers in clockwise order.

    Attributes
    ----------
    previous_move:  unicode literal
                    Previous move made by the agent.
    """
    previous_move = None

    def __init__(self, initial_move=Keys.ARROW_UP, clockwise=True):
        self.initial_move = initial_move
        self.clockwise = clockwise 

    def _set_previous_move(self, previous_move):
        """
        Sets the previous move made by the agent.

        Parameters
        ----------
        previous_move:  unicode literal
                        Previous move made by the agent corresponding to the 
                        Selenium webdriver common keys implementation.

        Returns
        -------
        None
        """
        self.previous_move = previous_move 

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
                    the Selenium webdriver common keys implementation.
        """
        # logic to sequentially loop through maneuvers
        if self.previous_move == Keys.ARROW_UP:
            next_move = Keys.ARROW_RIGHT if self.clockwise else Keys.ARROW_LEFT 
        elif self.previous_move == Keys.ARROW_RIGHT:
            next_move = Keys.ARROW_DOWN if self.clockwise else Keys.ARROW_UP
        elif self.previous_move == Keys.ARROW_DOWN:
            next_move = Keys.ARROW_LEFT if self.clockwise else Keys.ARROW_RIGHT 
        elif self.previous_move == Keys.ARROW_LEFT:
            next_move = Keys.ARROW_UP if self.clockwise else Keys.ARROW_DOWN
        else:
            next_move = self.initial_move 

        # update the previous move with the current move
        self._set_previous_move(next_move)

        return next_move 