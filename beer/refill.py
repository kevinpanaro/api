'''
Used basically as a main
'''
import logging
import os
from breweries import *
from breweries.helpers import *

def pour_beer():
    '''pour beer into the taps, heh...'''
    path = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(path, "beer.log")
    logLevel=logging.INFO
    FORMAT = '[%(asctime)s] [%(levelname)-8s] %(filename)-15s %(funcName)-18s - %(lineno)-3d - %(message)s'
    logging.basicConfig(filename=log_file, format=FORMAT,level=logLevel)

    reset_id()
    
    dock_street()
    equinox()
    evil_genius()
    mayorofoldtown()
    monks()
    odell()
    tired_hands()
    # TiredHands().update()

if __name__ == '__main__':
    pour_beer()
