'''
Used basically as a main
'''
from breweries.evilgenius import evil_genius
from breweries.tiredhands import tired_hands
from breweries.dockstreet import dock_street
from breweries.monks import monks
from breweries.equinox import equinox
from breweries.odell import odell


def pour_beer():
    '''pour beer into the taps, heh...'''
    evil_genius()
    tired_hands()
    dock_street()
    equinox()
    odell()
    # monks() # a later thing

if __name__ == '__main__':
    pour_beer()