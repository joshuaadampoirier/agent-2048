import os 
import http.server 
import socketserver 
from threading import Thread 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 


class GameEnv():
    """
    An object for the 2048 game environment. It can run the game on a server, 
    keep track of the game state, and interacts with the game.

    Parameters
    ----------
    path:   string 
            Folder path to the 2048 game repository.

    host:   string of four positive integers seperated by periods
            IP address of the host server.
    
    port:   positive integer
            Port to serve through.
    """
    def __init__(self, path, host='0.0.0.0', port=8000):
        self.path = path 
        self.host = host 
        self.port = port 

    def start_server(self):
        """
        Start the server running the game.

        Parameters
        ----------
        host:   string of four positive integers separated by periods.
                IP address of host. 
                Default: 0.0.0.0

        port:   positive integer
                Port to serve through. 
                Default: 8000

        Returns
        -------
        None
        """
        # move to the 2048 game directory
        os.chdir(os.path.expanduser(self.path))

        # create the server objects
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer((self.host, self.port), Handler)
        
        # start the server 
        httpd.serve_forever()

    def get_score(self, driver):
        """
        Retrieve the current score for this game.

        Parameters
        ----------
        driver:     webdriver object, connected to the game
                    Selenium Driver object for interfacing with the game.

        Returns
        -------
        score:      positive integer
                    Current score of this game. 

        score_add:  positive integer
                    Score added with last maneuver.
        """
        # retrieve the scores div element from the html
        elem = driver.find_element_by_css_selector('div.score-container')

        # parse scores out of the element
        scores = elem.text.split('+')

        # cast the scores to integers
        score = int(scores[0])
        if len(scores) == 2:
            score_add = int(scores[1])
        else:
            score_add = 0

        return score, score_add

    def get_tiles(self, driver):
        """
        Retrieve the current tiles and their locations.

        Parameters
        ----------
        driver:     webdriver object, connected to the game
                    Selenium Driver object for interfacing with the game.

        Returns
        -------
        tiles:      list of four lists, each four elements long
                    Each sublist represents a row starting from top to bottom.
                    Each element represents a tile, starting from left to right.
        """
        # initialize the tiles list
        tiles = [
            [None, None, None, None],   # top row
            [None, None, None, None],   # second row
            [None, None, None, None],   # third row
            [None, None, None, None]    # bottom row
        ]

        # loop through the tile html elements
        for elem in driver.find_elements_by_class_name('tile'):
            # retrieve the css classes assigned to the tile
            attr = elem.get_attribute('class')

            # parse row, column, value from css classes
            row = int(attr.split()[2].split('-')[3]) - 1
            col = int(attr.split()[2].split('-')[2]) - 1
            val = int(attr.split()[1].split('-')[1])

            # update the tiles list element; duplicates exist, be wary!
            if tiles[row][col] is None or val > tiles[row][col]:
                tiles[row][col] = val 

        return tiles
            

def main():
    """
    Build a game environment and play a few moves.

    Parameters
    ----------
        None

    Returns
    -------
        0
    """
    host = '0.0.0.0'
    port = 8000
    game = GameEnv(path='~/Documents/code/2048', host=host, port=port)
    
    thread = Thread(target=game.start_server)
    thread.start()

    # create a web driver for our game; using the Safari browser
    driver = webdriver.Safari() 
    driver.set_window_position(600, 0)
    driver.set_window_size(768, 768)

    # connect the driver to the server running the game
    driver.get("http://{h}:{p}".format(h=host, p=port))

    # retrieve the game element 
    elem = driver.find_element_by_class_name("game-container")

    # send a few game moves
    elem.send_keys(Keys.ARROW_DOWN)
    elem.send_keys(Keys.ARROW_DOWN)
    elem.send_keys(Keys.ARROW_RIGHT)
    elem.send_keys(Keys.ARROW_DOWN)
    elem.send_keys(Keys.ARROW_RIGHT)

    # get and print the current score 
    score, _ = game.get_score(driver)
    print(score)

    # get and print the current tiles
    tiles = game.get_tiles(driver)
    print(tiles)

    return 0


if __name__ == '__main__':
    main()