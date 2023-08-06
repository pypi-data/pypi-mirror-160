"""
isHex
https://github.com/xhelphin/ishex

Simple Python package to check if string is valid hexadecimal.
"""

def isHex(string):
    """
    Returns True if string is valid hexidecimal, else returns False.
    """
    validCharacters = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    string = string.lower()
    for character in string:
        if character not in validCharacters:
            return False
    return True