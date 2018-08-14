'''
Used basically as a main
'''
import logging
from breweries import *
from breweries.helpers import *

def pour_beer():
    '''pour beer into the taps, heh...'''
    logLevel=logging.INFO
    FORMAT = '[%(asctime)s] [%(levelname)-8s] %(filename)-15s %(funcName)-18s - %(lineno)-3d - %(message)s'
    logging.basicConfig(format=FORMAT,level=logLevel)

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
