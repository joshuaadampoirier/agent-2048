import os 
import pickle 
from threading import Thread 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 

from agents.sequential import SequentialAgent 
from envs.env import GameEnv


def create_agent(filename='demo.pkl'):
    """
    Create and save a simple agent to a file.

    Parameters
    ----------
    filename:       string
                    File name to the created file.

    Returns
    -------
    None
    """
    # delete the file if it exists - we will overwrite
    if os.path.exists(filename):
        os.remove(filename)

    # create and save agent to pickle file
    agent = SequentialAgent() 
    agent.save(filename=filename)


def main():
    """
    Load a Sequential agent to play the game.

    Parameters
    ----------
        None

    Returns
    -------
        0
    """
    # build game environment
    game = GameEnv(path='~/Documents/code/2048')

    # load agent from pickle file
    filename = 'demo.pkl'
    create_agent(filename)
    agent = pickle.load(open(filename, 'rb'))
    
    thread = Thread(target=game.start_server)
    thread.start()

    # create a web driver for our game; using the Safari browser
    driver = webdriver.Safari() 
    driver.set_window_position(600, 0)
    driver.set_window_size(768, 768)

    # connect the driver to the server running the game
    driver.get("http://{h}:{p}".format(h=game.host, p=game.port))

    # retrieve the game element 
    elem = driver.find_element_by_class_name("game-container")

    # loop through a full game
    i = 0
    while game.get_condition(driver) != game.game_over and i < game.max_iter:
        # make the agents next move
        elem.send_keys(agent.next_move())

        # retrieve the updated game state
        score, _ = game.get_score(driver)
        condition = game.get_condition(driver)

        # inform the user of the updated game state
        print('Iter: {iter}, New score: {s}, Condition: {c}'.format(
            iter=i,
            s=score,
            c=condition
        ))

        i += 1

    return 0


if __name__ == '__main__':
    main()