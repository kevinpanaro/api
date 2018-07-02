import unicodedata

def unicode_to_ascii(string):
    string = unicodedata.normalize('NFKD', string.strip()).encode('ascii', 'ignore')
    return string