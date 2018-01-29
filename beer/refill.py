'''
Used basically as a main
'''
from breweries.evilgenius import evil_genius
from breweries.tiredhands import tired_hands


def pour_beer():
    '''pour beer into the taps, heh...'''
    evil_genius()
    tired_hands()

if __name__ == '__main__':
    pour_beer()