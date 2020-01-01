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
    content = driver.find_element_by_css_selector('div.score-container')
    print(content.text)

    return 0


if __name__ == '__main__':
    main()