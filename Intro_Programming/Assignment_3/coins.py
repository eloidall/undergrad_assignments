import doctest

BASE8_CHARS   = '01234567'
BASE202_CHARS = '0C2OMPIN'

def base10_to_202(amt_in_base10):
    ''' (int) -> str
    >>> base10_to_202(202)
    '0c00000OC2'
    '''
    octal_s = oct(amt_in_base10)
    
    new_s = '0c'
    for i in range(8-len(octal_s)+2):
        new_s = new_s + '0'
    for c in octal_s[2:]:
        new_s = new_s + BASE202_CHARS[int(c)]
    return new_s

def is_base202(text):
    """ (str) -> bool
    10 character string
    
    >>> is_base202('1cCOMPCOIN')
    False
    >>> is_base202('0c0C2OMPIN')
    True
    """
    if len(text) != 10:
        return False
    if text[0:2].lower() != '0c':
        return False
    for c in text[2:]:
        if c.upper() not in BASE202_CHARS:
            return False
    return True

if __name__ == '__main__':
    doctest.testmod()