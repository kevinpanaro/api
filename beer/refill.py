'''
Used basically as a main
'''

from breweries import *
# from breweries.threefourbeerco import threefourbeerco
# from breweries.tiredhands_class import TiredHands


def pour_beer():
    '''pour beer into the taps, heh...'''
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
