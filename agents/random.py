from random import randint

from agents.base import BaseAgent
from selenium.webdriver.common.keys import Keys 


class RandomAgent(BaseAgent):
    """
    Class object for the random agent.

    This agent is governed by simple logic. Given a seed for the random number
    generator, a random next move is chosen.

    Parameters
    ----------
    seed:   integer, default 1234
            Seed for the random number generator.
    """
    def __init__(self, seed=1234):
        self.seed = seed

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
        # place all move possibilities into a list
        moves = [
            Keys.ARROW_UP, 
            Keys.ARROW_RIGHT, 
            Keys.ARROW_DOWN, 
            Keys.ARROW_LEFT
        ]
        
        # randomly pick the next move
        next_move = moves[randint(0, 3)]

        return next_move 