from threading import Thread 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 

from agents.sequential import SequentialAgent 
from envs.env import GameEnv


def main():
    """
    Build a Sequential agent to play the game.

    Parameters
    ----------
        None

    Returns
    -------
        0
    """
    game = GameEnv(path='~/Documents/code/2048')
    agent = SequentialAgent()
    
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