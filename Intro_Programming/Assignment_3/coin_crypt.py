# Author: Éloi Dallaire
# McGill ID: 260794674

import doctest
from coin_utils import *


def get_crypt_dictionary(keys, value_generator):
    """ (list, function) -> dict

    This function takes as input a keys list and a function value_generator and returns a
    dictionary with keys from the input list and value generated by the input function.

    >>> random.seed(9001)
    >>> get_crypt_dictionary(['a', 'b', 'c'], get_random_comp202coin)
    {'a': '0c0MPNN0OC', 'b': '0cMIMNIO0P', 'c': '0cM0OCCIOI'}
    
    >>> random.seed(9001)
    >>> get_crypt_dictionary(['a', 'b', 'c'], get_random_character)
    {'a': 't', 'b': 'è', 'c': '7'}
    
    >>> random.seed(88)
    >>> get_crypt_dictionary(['aaa', 'bbb', 100, 200, 'x', 'y'], get_random_comp202coin)
    {'aaa': '0cI2N0CIPC', 'bbb': '0cO020OIPC', 100: '0cP2MI2N2C', 200: '0c2NPO2NCI', 'x': '0c0CII0ONN', 'y': '0c0C0000II'}
    
    >>> get_crypt_dictionary(3333, get_random_comp202coin)
    Traceback (most recent call last):
    AssertionError: the first input must be of type list
    
    >>> get_crypt_dictionary([1, 2, 'aaa', 'aaa', 2, 3], get_random_comp202coin)
    Traceback (most recent call last):
    AssertionError: duplicate keys found
    
    >>> keys = list(ALPHABET) + list(PUNCTUATION) + ['aa', 'bb', 'cc']
    >>> get_crypt_dictionary(keys, get_random_comp202coin)
    Traceback (most recent call last):
    AssertionError: the input list must not have more element than charcaters contained in ALL_CHARACTERS
    """
    # Input Validation
    if type(keys) != list:
        raise AssertionError("the first input must be of type list")
    if len(keys) != len(get_unique_elements(keys)):
        raise AssertionError("duplicate keys found")
    if len(keys) > len(ALL_CHARACTERS):
        raise AssertionError("the input list must not have more element than charcaters contained in ALL_CHARACTERS")
    
    # To create a copy of the list taken as input
    keys_copy = keys[:]
    
    # To create the dictionary using the value_generator function
    output_dict = {}
    for i, x in enumerate(keys_copy):
        value_generated = value_generator(i)
        # To ensure we have all unique values in output_dict
        while value_generated in output_dict:
            value_generated = value_generator(i)    
        output_dict[x] = value_generated
        
    return output_dict


def encrypt_text(text):
    """ (str) -> tuple(str, dict)

    This function takes as input a string and returns a tuple containing a string
    representing a random COMP202COIN for each unique charcaters from the input string
    and also a dictionary mapping each unique charcaters as keys to its random COMP202COIN.

    >>> random.seed(9001)
    >>> (s, d) = encrypt_text('too')
    >>> s
    '0c0MPNN0OC-0cMIMNIO0P-0cMIMNIO0P'
    >>> d
    {'t': '0c0MPNN0OC', 'o': '0cMIMNIO0P'}
    
    >>> random.seed(222)
    >>> encrypt_text('GGGG11')
    ('0cCPIONCNM-0cCPIONCNM-0cCPIONCNM-0cCPIONCNM-0cOI0NC02P-0cOI0NC02P', {'g': '0cCPIONCNM', '1': '0cOI0NC02P'})
    
    >>> random.seed(111)
    >>> (s1, d1) = encrypt_text('COCO oil')
    >>> s1
    '0cOOCINPCC-0cP0OMOPP0-0cOOCINPCC-0cP0OMOPP0-0cNNCICMCO-0cP0OMOPP0-0cO0IINP2N-0cI2NC02CO'
    >>> d1['o']
    '0cP0OMOPP0'
    
    >>> encrypt_text(232323)
    Traceback (most recent call last):
    AssertionError: the input must be of type string
    """
    # Input Validation
    if type(text) != str:
        raise AssertionError("the input must be of type string")
    
    # To create a lower case copy of the string taken as input
    text_copy = text.lower()
    # To ensure every characters are contained in ALL_CHARACTERS
    for char in text_copy:
        if char not in ALL_CHARACTERS:
            raise AssertionError("characters of the input string must be present in ALL_CHARACTERS")    
    
    # To create the dictionary with unique keys
    keys = get_unique_elements(list(text_copy))
    output_dict = get_crypt_dictionary(keys, get_random_comp202coin)
    
    # To create the final string
    output_str_list = []
    for char in text_copy:
        output_str_list.append(output_dict[char])
    output_str = '-'.join(output_str_list)    
    
    # To return the final string and the dictionary in a tuple
    return (output_str, output_dict)


def encrypt_file(filename):
    """ (str) -> dict

    This function takes as input a filename and returns an
    encrypted dictionary corresponding to the content of the file.

    >>> random.seed(42)
    >>> encrypt_file('dubliners.txt')
    {'t': '0cCI200CM2', 'h': '0c0OCMN0IP', 'e': '0cMOCP02MM', ' ': '0cON2ICCIN', 'p': '0cOMMMM2PP', 'r': '0c2CIN0I0O', 'o': '0cCP0NP0NN', 'j': '0cCOC0CMNN', 'c': '0cII00O0MO', 'g': '0c0M0M2N2C', 'u': '0c0OIM0I2M', 'n': '0cCONNMO22', 'b': '0cOONN0P2C', 'k': '0cOPICNP2M', 'f': '0c0OOCO0ON', 'd': '0cOCOMN0CM', 'l': '0cIPPMPPCP', 'i': '0cOMCPII2N', 's': '0cNCONN2N2', ',': '0cMOMINM0O', 'y': '0c00IPCNCI', 'a': '0c2MOONOOP', 'm': '0cII0I0OP2', '\\n': '0cPOMO2P20', 'w': '0cMOMM2MMN', 'v': '0c2ONCPM02', '.': '0cOOMOIIO2', '-': '0cPO0PO0OI', ':': '0cCP0P2OMN', '2': '0cCOINICM2', '0': '0cI0P02N2M', '1': '0cCMO02OCN', '[': '0cPPNMI0MP', '#': '0cPM0CPOII', '8': '0cMCIINP0N', '4': '0c0PMONMM2', ']': '0cN2IOMINM', '9': '0cCNNIMMII', '*': '0cI0OMNP02', 'z': '0cC20PMCNN', '(': '0cMPMCPPII', ')': '0cPI22M0NC', 'q': '0cO0MNCIMI', '"': '0cC0NCI2NO', "'": '0c0PINOCCO', 'x': '0cOPC2NM2P', '!': '0cMP02P2P0', ';': '0cC2CPPCNI', '?': '0cOPIO0COP', '_': '0cCMNOOCIP', '5': '0cI0PCNNMN', 'é': '0cMOMPC2CI', 'è': '0cN2022PMP', 'ç': '0cPIPMPPC0', '&': '0c2MIMOPMP', 'æ': '0cPNO0MCOM', '7': '0cPPOIO0C2', '6': '0cO2IM220C', 'œ': '0cM2CO0P2C', '/': '0cCCC0NOOI', '3': '0c2PNCNPNM', '%': '0cON2PONOO', '@': '0c2MN2MPNP', '$': '0cNOC2IPOI'}
    
    >>> random.seed(1111)
    >>> encrypt_file('common_words.txt')
    {'m': '0cOOIIMPOI', 'e': '0cOC22PPNM', '\\n': '0cPM0PC2PO', 'y': '0c22C2OOP2', 's': '0cPIMINI0M', 'l': '0cNCCNOCNC', 'f': '0cC2PMI0I2', 'w': '0c2NNNOPPI', 'o': '0cCONMIMMN', 'u': '0cPO22PCCI', 'r': '0cCPP0IPIO', 'v': '0cN0CCPICO', 'h': '0c22N2PCNN', 'i': '0c2IP2INOI', 't': '0cM2NMMIPO', 'a': '0c0P2I2ICN', 'c': '0cPNM0MMPI', 'b': '0cNP220INO', 'n': '0cMMPNNIOM', 'g': '0cPMOIOP0P', 'd': '0cMNN0NMMM', 'p': '0cOONCPPNI', 'j': '0c200CMCNM'}
    
    >>> encrypt_file(4444)
    Traceback (most recent call last):
    AssertionError: the input must be of type string
    """
    # Input validation
    if type(filename) != str:
        raise AssertionError("the input must be of type string")
    
    fobj = open(filename, 'r', encoding='utf-8')
    text_str = ''
    for line in fobj:
        for char in line:
            text_str += char
    fobj.close()
    
    # To encrypt
    (output_str, output_dict) = encrypt_text(text_str)
    
    # To store the string in a new file
    encrypted_filename = filename.strip('.txt') + '_encrypted' + '.txt'
    fobj1 = open(encrypted_filename, 'w', encoding='utf-8')
    fobj1.write(output_str)
    fobj1.close()
    # To return the dictionary
    return output_dict


def decrypt_text(text, decryption_dict):
    """ (str, dict) -> str

    This function takes as argument a string encypted in COMP202COIN
    and a decryption dictionary and returns the decrypted string.

    >>> d = {'0c0MPNN0OC': 'a', '0cMIMNIO0P': 'b', '0cM0OCCIOI': 'c'}
    >>> decrypt_text('0c0MPNN0OC-0cM0OCCIOI-0c0MPNN0OC', d)
    'aca'
    
    >>> d1 = {'0cMMMMmmmm': 'm', '0cNNNNnnnn': 'n', '0cOOOOoooo': 'o', '0cPPPPpppp': 'p'}
    >>> decrypt_text('0cPPPPpppp-0cOOOOoooo-0cMMMMmmmm-0cPPPPpppp-0cOOOOoooo-0cMMMMmmmm', d1)
    'pompom'
    
    >>> decrypt_text('0cMMMMmmmm-0cOOOOoooo-0cPPPPpppp', d1)
    'mop'
    
    >>> decrypt_text(11111, 'hello')
    Traceback (most recent call last):
    AssertionError: the inputs must be of type string and dictionary respectively
    
    >>> d = {'0c0MPNN0OC': 'a', '0cMIMNIO0P': 'b', '0cM0OCCIOI': 'c'}
    >>> decrypt_text('0c0MPNN0OC akswdhuwhduwhs', d)
    Traceback (most recent call last):
    AssertionError: the first input string must only consist of valid COMP202COIN separated by hyphens
    
    >>> d = {'0c0MPNN0OC': 'a', '0cMIMNIO0P': 'b', '0cM0OCCIOI': 'c'}
    >>> decrypt_text('0c0MPNN0OC-0cMMMMMMMM', d)
    Traceback (most recent call last):
    AssertionError: some COMP202COIN present in the string are not part of the dictionary
    """
    # Input Validation
    if (type(text), type(decryption_dict)) != (str, dict):
        raise AssertionError("the inputs must be of type string and dictionary respectively")
    
    # To create a copy of the inputs
    text_copy = text
    decryption_dict_copy = decryption_dict
    
    # To get a list of all COINs from the string
    valid_coins = get_all_coins(text_copy)
    # To initialize the output string
    output_str = ''
   
    # Error Handling
    if text_copy.split('-') != valid_coins:
        raise AssertionError("the first input string must only consist of valid COMP202COIN separated by hyphens")
    # To iterate through each valid COIN
    for e in valid_coins:
        if e not in decryption_dict_copy:
            raise AssertionError("some COMP202COIN present in the string are not part of the dictionary")
        # To return the value mapped to each COIN
        else:
            output_str += decryption_dict_copy[e]      
    return output_str


def decrypt_file(filename, decryption_dict):
    """ (str, dict) -> NoneType

    This funciton takes as input a str representing a filename and a dictionary.
    It will decrypt the content of the file with the content of the dictionary.

    >>> decrypt_file('dubliners_encrypted.txt', reverse_dict(encrypt_file('dubliners.txt')))
    >>> fobj = open('dubliners.txt', 'r', encoding='utf-8')
    >>> fobj2 = open('dubliners_encrypted_decrypted.txt', 'r', encoding='utf-8')
    >>> fobj.read().lower() == fobj2.read()
    True
    
    >>> decrypt_file('common_words_encrypted.txt', reverse_dict(encrypt_file('common_words.txt')))
    >>> fobj = open('common_words.txt', 'r', encoding='utf-8')
    >>> fobj2 = open('common_words_encrypted_decrypted.txt', 'r', encoding='utf-8')
    >>> fobj.read().lower() == fobj2.read()
    True
    
    >>> decrypt_file('common_words_encrypted.txt' , 121212)
    Traceback (most recent call last):
    AssertionError: the inputs must be of type string and dictionary respectively
    """
    # Input Validation
    if (type(filename), type(decryption_dict)) != (str, dict):
        raise AssertionError("the inputs must be of type string and dictionary respectively")
    
    # Create a copy of the string in _encrypted.txt
    fobj = open(filename, 'r', encoding='utf-8')
    text_str = ''
    for char in fobj:
        text_str += char
    fobj.close()
    
    # To decrypt
    output_str = decrypt_text(text_str, decryption_dict)

    # To store the string in a new file
    encrypted_decrypted_filename = filename.strip('.txt') + '_decrypted' + '.txt'
    fobj2 = open(encrypted_decrypted_filename, 'w', encoding='utf-8')
    fobj2.write(output_str)
    fobj2.close()



def random_decrypt(encrypted_s, n, common_words_filename): 
    """ (str, int, str) -> str

    This function takes as input an encrypted string, a positive integer n
    and a string representing the name of a file. It returns the best possible
    decryption of the input string, based on each try percentage of common words.
    
    >>> random.seed(49)
    >>> encrypted_s = '0c0MPNN0OC-0cMIMNIO0P-0cMIMNIO0P'
    >>> random_decrypt(encrypted_s, 10**3, 'common_words.txt')
    'too'
    
    >>> random.seed(49)
    >>> random_decrypt(encrypted_s, 10**2, 'common_words.txt')
    'f33'
    
    >>> random.seed(223)
    >>> encrypted_s1 = '0cPPPPpppp-0cOOOOoooo-0cMMMMmmmm-0cCCCCcccc'
    >>> random_decrypt(encrypted_s1, 1200 , 'common_words.txt')
    '.`we'
    
    >>> random.seed(9007)
    >>> encrypted_s2 = '0cPPPPpppp-0cOOOOoooo-0cMMMMmmmm-0cCCCCcccc-0c00000000-0cIIIIiiii-0cI2222222-0cIIII0000-0cIIIIiii0-0cOOOO0000-0cIIIIiiii-0cCCCC0000-0cMMMM0000-0cCCCCccII-0cCCCCccPP-0cCCCCcopI'
    >>> random_decrypt(encrypted_s2, 1200 , 'common_words.txt')
    ' an,3`"or;`~&>_='
    
    >>> random_decrypt(encrypted_s, 12.111, 1212)
    Traceback (most recent call last):
    AssertionError: the inputs must be of type string, integer and string respectively
    
    >>> random_decrypt(encrypted_s, -9, 'common_words.txt')
    Traceback (most recent call last):
    AssertionError: the integer input must be positive
    
    >>> encrypted_s = '0c0MPNN0OC- sskdsj o2929 292'
    >>> random_decrypt(encrypted_s, 100, 'common_words.txt')
    Traceback (most recent call last):
    AssertionError: the first input string must only consist of valid COMP202COIN separated by hyphens
    """
    # Input Validation
    if (type(encrypted_s), type(n), type(common_words_filename)) != (str, int, str):
        raise AssertionError("the inputs must be of type string, integer and string respectively")
    if n <= 0:
        raise AssertionError("the integer input must be positive")
    
    # To get a list of all COINs from the string
    valid_coins = get_all_coins(encrypted_s)
    
    # Error Handling
    if encrypted_s.split('-') != valid_coins:
        raise AssertionError("the first input string must only consist of valid COMP202COIN separated by hyphens")
    
    # To get unique coins
    unique_coins = get_unique_elements(valid_coins)
    
    # To initialize the output tuple
    best_decryption = ('', 0) 
    
    for attempt in range(n):
        # To create a dictionary for each decryption attempt
        decrypted_dict = get_crypt_dictionary(unique_coins, get_random_character)
        
        # To create a string with all values of the dictionary
        decrypted_str = ''
        for coins in valid_coins:
            decrypted_str += decrypted_dict[coins]
                
        # To update the best_decryption if it's better
        performance = get_pct_common_words(decrypted_str, common_words_filename)
        if performance >= best_decryption[1]:
            best_decryption = (decrypted_str, performance)
        
    return best_decryption[0]



def decrypt_with_user_input(encrypted_s):
    """ (str) -> str

    This function takes an encrypted string and allows to decrypt it
    using the user input and based on English language letter frequency.

    >>> random.seed(138)
    >>> s, d = encrypt_text("The spelling of English words is not fixed and invariable, nor does it depend on any other authority than general agreement. At the present day there is practically unanimous agreement as to the spelling of most words. In the list below, for example, 'rime' for 'rhyme' is the only allowable variation; all the other forms are co-extensive with the English language. At any given moment, however, a relatively small number of words may be spelled in more than one way. Gradually, as a rule, one of these forms comes to be generally preferred, and the less customary form comes to look obsolete and is discarded. From time to time new forms, mostly simplifications, are introduced by innovators, and either win their place or die of neglect.")

    >>> s = decrypt_with_user_input(s)
    Decrypted string: THE SUELLING OY ENGLISH PORDS IS NOT YI,ED AND INXARIAVLEC NOR DOES IT DEUEND ON ANF OTHER ABTHORITF THAN GENERAL AGREEMENTK AT THE URESENT DAF THERE IS URAWTIWALLF BNANIMOBS AGREEMENT AS TO THE SUELLING OY MOST PORDSK IN THE LIST VELOPC YORE,AMULEC .RIME. YOR .RHFME. IS THE ONLF ALLOPAVLE XARIATION" ALL THE OTHER YORMS ARE WO-E,TENSIXE PITH THE ENGLISH LANGBAGEK AT ANF GIXEN MOMENTC HOPEXERC A RELATIXELF SMALL NBMVER OY PORDS MAF VE SUELLED IN MORE THAN ONE PAFK GRADBALLFC AS A RBLEC ONE OY THESE YORMS WOMES TO VE GENERALLF UREYERREDC AND THE LESS WBSTOMARF YORM WOMES TO LOO' OVSOLETE AND IS DISWARDEDK YROM TIME TO TIME NEP YORMSC MOSTLF SIMULIYIWATIONSC ARE INTRODBWED VF INNOXATORSC AND EITHER PIN THEIR ULAWE OR DIE OY NEGLEWTK
    End decryption? n
    Enter first letter to swap: U
    Enter second letter to swap: P
    Decrypted string: THE SPELLING OY ENGLISH UORDS IS NOT YI,ED AND INXARIAVLEC NOR DOES IT DEPEND ON ANF OTHER ABTHORITF THAN GENERAL AGREEMENTK AT THE PRESENT DAF THERE IS PRAWTIWALLF BNANIMOBS AGREEMENT AS TO THE SPELLING OY MOST UORDSK IN THE LIST VELOUC YOR E,AMPLEC .RIME. YOR .RHFME. IS THE ONLF ALLOUAVLE XARIATION" ALL THE OTHER YORMS ARE WO-E,TENSIXE UITH THE ENGLISH LANGBAGEK AT ANF GIXEN MOMENTC HOUEXERC A RELATIXELF SMALL NBMVER OY UORDS MAF VE SPELLED IN MORE THAN ONE UAFK GRADBALLFC AS A RBLEC ONE OY THESE YORMS WOMES TO VE GENERALLF PREYERREDC AND THE LESS WBSTOMARF YORM WOMES TO LOO' OVSOLETE AND IS DISWARDEDK YROM TIME TO TIME NEU YORMSC MOSTLF SIMPLIYIWATIONSC ARE INTRODBWED VF INNOXATORSC AND EITHER UIN THEIR PLAWE OR DIE OY NEGLEWTK
    End decryption? n
    Enter first letter to swap: Y
    Enter second letter to swap: F
    Decrypted string: THE SPELLING OF ENGLISH UORDS IS NOT FI,ED AND INXARIAVLEC NOR DOES IT DEPEND ON ANY OTHER ABTHORITY THAN GENERAL AGREEMENTK AT THE PRESENT DAY THERE IS PRAWTIWALLY BNANIMOBS AGREEMENT AS TO THE SPELLING OF MOST UORDSK IN THE LIST VELOUC FOR E,AMPLEC .RIME. FOR .RHYME. IS THE ONLY ALLOUAVLE XARIATION" ALL THE OTHER FORMS ARE WO-E,TENSIXE UITH THE ENGLISH LANGBAGEK AT ANY GIXEN MOMENTC HOUEXERC A RELATIXELY SMALL NBMVER OF UORDS MAY VE SPELLED IN MORE THAN ONE UAYK GRADBALLYC AS A RBLEC ONE OF THESE FORMS WOMES TO VE GENERALLY PREFERREDC AND THE LESS WBSTOMARY FORM WOMES TO LOO' OVSOLETE AND IS DISWARDEDK FROM TIME TO TIME NEU FORMSC MOSTLY SIMPLIFIWATIONSC ARE INTRODBWED VY INNOXATORSC AND EITHER UIN THEIR PLAWE OR DIE OF NEGLEWTK
    End decryption? n
    Enter first letter to swap: U
    Enter second letter to swap: W
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FI,ED AND INXARIAVLEC NOR DOES IT DEPEND ON ANY OTHER ABTHORITY THAN GENERAL AGREEMENTK AT THE PRESENT DAY THERE IS PRAUTIUALLY BNANIMOBS AGREEMENT AS TO THE SPELLING OF MOST WORDSK IN THE LIST VELOWC FOR E,AMPLEC .RIME. FOR .RHYME. IS THE ONLY ALLOWAVLE XARIATION" ALL THE OTHER FORMS ARE UO-E,TENSIXE WITH THE ENGLISH LANGBAGEK AT ANY GIXEN MOMENTC HOWEXERC A RELATIXELY SMALL NBMVER OF WORDS MAY VE SPELLED IN MORE THAN ONE WAYK GRADBALLYC AS A RBLEC ONE OF THESE FORMS UOMES TO VE GENERALLY PREFERREDC AND THE LESS UBSTOMARY FORM UOMES TO LOO' OVSOLETE AND IS DISUARDEDK FROM TIME TO TIME NEW FORMSC MOSTLY SIMPLIFIUATIONSC ARE INTRODBUED VY INNOXATORSC AND EITHER WIN THEIR PLAUE OR DIE OF NEGLEUTK
    End decryption? n
    Enter first letter to swap: ,
    Enter second letter to swap: X
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FIXED AND IN,ARIAVLEC NOR DOES IT DEPEND ON ANY OTHER ABTHORITY THAN GENERAL AGREEMENTK AT THE PRESENT DAY THERE IS PRAUTIUALLY BNANIMOBS AGREEMENT AS TO THE SPELLING OF MOST WORDSK IN THE LIST VELOWC FOR EXAMPLEC .RIME. FOR .RHYME. IS THE ONLY ALLOWAVLE ,ARIATION" ALL THE OTHER FORMS ARE UO-EXTENSI,E WITH THE ENGLISH LANGBAGEK AT ANY GI,EN MOMENTC HOWE,ERC A RELATI,ELY SMALL NBMVER OF WORDS MAY VE SPELLED IN MORE THAN ONE WAYK GRADBALLYC AS A RBLEC ONE OF THESE FORMS UOMES TO VE GENERALLY PREFERREDC AND THE LESS UBSTOMARY FORM UOMES TO LOO' OVSOLETE AND IS DISUARDEDK FROM TIME TO TIME NEW FORMSC MOSTLY SIMPLIFIUATIONSC ARE INTRODBUED VY INNO,ATORSC AND EITHER WIN THEIR PLAUE OR DIE OF NEGLEUTK
    End decryption? n
    Enter first letter to swap: C
    Enter second letter to swap: ,
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FIXED AND INCARIAVLE, NOR DOES IT DEPEND ON ANY OTHER ABTHORITY THAN GENERAL AGREEMENTK AT THE PRESENT DAY THERE IS PRAUTIUALLY BNANIMOBS AGREEMENT AS TO THE SPELLING OF MOST WORDSK IN THE LIST VELOW, FOR EXAMPLE, .RIME. FOR .RHYME. IS THE ONLY ALLOWAVLE CARIATION" ALL THE OTHER FORMS ARE UO-EXTENSICE WITH THE ENGLISH LANGBAGEK AT ANY GICEN MOMENT, HOWECER, A RELATICELY SMALL NBMVER OF WORDS MAY VE SPELLED IN MORE THAN ONE WAYK GRADBALLY, AS A RBLE, ONE OF THESE FORMS UOMES TO VE GENERALLY PREFERRED, AND THE LESS UBSTOMARY FORM UOMES TO LOO' OVSOLETE AND IS DISUARDEDK FROM TIME TO TIME NEW FORMS, MOSTLY SIMPLIFIUATIONS, ARE INTRODBUED VY INNOCATORS, AND EITHER WIN THEIR PLAUE OR DIE OF NEGLEUTK
    End decryption? n
    Enter first letter to swap: V
    Enter second letter to swap: B
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FIXED AND INCARIABLE, NOR DOES IT DEPEND ON ANY OTHER AVTHORITY THAN GENERAL AGREEMENTK AT THE PRESENT DAY THERE IS PRAUTIUALLY VNANIMOVS AGREEMENT AS TO THE SPELLING OF MOST WORDSK IN THE LIST BELOW, FOR EXAMPLE, .RIME. FOR .RHYME. IS THE ONLY ALLOWABLE CARIATION" ALL THE OTHER FORMS ARE UO-EXTENSICE WITH THE ENGLISH LANGVAGEK AT ANY GICEN MOMENT, HOWECER, A RELATICELY SMALL NVMBER OF WORDS MAY BE SPELLED IN MORE THAN ONE WAYK GRADVALLY, AS A RVLE, ONE OF THESE FORMS UOMES TO BE GENERALLY PREFERRED, AND THE LESS UVSTOMARY FORM UOMES TO LOO' OBSOLETE AND IS DISUARDEDK FROM TIME TO TIME NEW FORMS, MOSTLY SIMPLIFIUATIONS, ARE INTRODVUED BY INNOCATORS, AND EITHER WIN THEIR PLAUE OR DIE OF NEGLEUTK
    End decryption? n
    Enter first letter to swap: C
    Enter second letter to swap: V
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FIXED AND INVARIABLE, NOR DOES IT DEPEND ON ANY OTHER ACTHORITY THAN GENERAL AGREEMENTK AT THE PRESENT DAY THERE IS PRAUTIUALLY CNANIMOCS AGREEMENT AS TO THE SPELLING OF MOST WORDSK IN THE LIST BELOW, FOR EXAMPLE, .RIME. FOR .RHYME. IS THE ONLY ALLOWABLE VARIATION" ALL THE OTHER FORMS ARE UO-EXTENSIVE WITH THE ENGLISH LANGCAGEK AT ANY GIVEN MOMENT, HOWEVER, A RELATIVELY SMALL NCMBER OF WORDS MAY BE SPELLED IN MORE THAN ONE WAYK GRADCALLY, AS A RCLE, ONE OF THESE FORMS UOMES TO BE GENERALLY PREFERRED, AND THE LESS UCSTOMARY FORM UOMES TO LOO' OBSOLETE AND IS DISUARDEDK FROM TIME TO TIME NEW FORMS, MOSTLY SIMPLIFIUATIONS, ARE INTRODCUED BY INNOVATORS, AND EITHER WIN THEIR PLAUE OR DIE OF NEGLEUTK
    End decryption? n
    Enter first letter to swap: C
    Enter second letter to swap: U
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FIXED AND INVARIABLE, NOR DOES IT DEPEND ON ANY OTHER AUTHORITY THAN GENERAL AGREEMENTK AT THE PRESENT DAY THERE IS PRACTICALLY UNANIMOUS AGREEMENT AS TO THE SPELLING OF MOST WORDSK IN THE LIST BELOW, FOR EXAMPLE, .RIME. FOR .RHYME. IS THE ONLY ALLOWABLE VARIATION" ALL THE OTHER FORMS ARE CO-EXTENSIVE WITH THE ENGLISH LANGUAGEK AT ANY GIVEN MOMENT, HOWEVER, A RELATIVELY SMALL NUMBER OF WORDS MAY BE SPELLED IN MORE THAN ONE WAYK GRADUALLY, AS A RULE, ONE OF THESE FORMS COMES TO BE GENERALLY PREFERRED, AND THE LESS CUSTOMARY FORM COMES TO LOO' OBSOLETE AND IS DISCARDEDK FROM TIME TO TIME NEW FORMS, MOSTLY SIMPLIFICATIONS, ARE INTRODUCED BY INNOVATORS, AND EITHER WIN THEIR PLACE OR DIE OF NEGLECTK
    End decryption? n
    Enter first letter to swap: K
    Enter second letter to swap: .
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FIXED AND INVARIABLE, NOR DOES IT DEPEND ON ANY OTHER AUTHORITY THAN GENERAL AGREEMENT. AT THE PRESENT DAY THERE IS PRACTICALLY UNANIMOUS AGREEMENT AS TO THE SPELLING OF MOST WORDS. IN THE LIST BELOW, FOR EXAMPLE, KRIMEK FOR KRHYMEK IS THE ONLY ALLOWABLE VARIATION" ALL THE OTHER FORMS ARE CO-EXTENSIVE WITH THE ENGLISH LANGUAGE. AT ANY GIVEN MOMENT, HOWEVER, A RELATIVELY SMALL NUMBER OF WORDS MAY BE SPELLED IN MORE THAN ONE WAY. GRADUALLY, AS A RULE, ONE OF THESE FORMS COMES TO BE GENERALLY PREFERRED, AND THE LESS CUSTOMARY FORM COMES TO LOO' OBSOLETE AND IS DISCARDED. FROM TIME TO TIME NEW FORMS, MOSTLY SIMPLIFICATIONS, ARE INTRODUCED BY INNOVATORS, AND EITHER WIN THEIR PLACE OR DIE OF NEGLECT.
    End decryption? n
    Enter first letter to swap: K
    Enter second letter to swap: '
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FIXED AND INVARIABLE, NOR DOES IT DEPEND ON ANY OTHER AUTHORITY THAN GENERAL AGREEMENT. AT THE PRESENT DAY THERE IS PRACTICALLY UNANIMOUS AGREEMENT AS TO THE SPELLING OF MOST WORDS. IN THE LIST BELOW, FOR EXAMPLE, 'RIME' FOR 'RHYME' IS THE ONLY ALLOWABLE VARIATION" ALL THE OTHER FORMS ARE CO-EXTENSIVE WITH THE ENGLISH LANGUAGE. AT ANY GIVEN MOMENT, HOWEVER, A RELATIVELY SMALL NUMBER OF WORDS MAY BE SPELLED IN MORE THAN ONE WAY. GRADUALLY, AS A RULE, ONE OF THESE FORMS COMES TO BE GENERALLY PREFERRED, AND THE LESS CUSTOMARY FORM COMES TO LOOK OBSOLETE AND IS DISCARDED. FROM TIME TO TIME NEW FORMS, MOSTLY SIMPLIFICATIONS, ARE INTRODUCED BY INNOVATORS, AND EITHER WIN THEIR PLACE OR DIE OF NEGLECT.
    End decryption? n
    Enter first letter to swap: "
    Enter second letter to swap: ;
    Decrypted string: THE SPELLING OF ENGLISH WORDS IS NOT FIXED AND INVARIABLE, NOR DOES IT DEPEND ON ANY OTHER AUTHORITY THAN GENERAL AGREEMENT. AT THE PRESENT DAY THERE IS PRACTICALLY UNANIMOUS AGREEMENT AS TO THE SPELLING OF MOST WORDS. IN THE LIST BELOW, FOR EXAMPLE, 'RIME' FOR 'RHYME' IS THE ONLY ALLOWABLE VARIATION; ALL THE OTHER FORMS ARE CO-EXTENSIVE WITH THE ENGLISH LANGUAGE. AT ANY GIVEN MOMENT, HOWEVER, A RELATIVELY SMALL NUMBER OF WORDS MAY BE SPELLED IN MORE THAN ONE WAY. GRADUALLY, AS A RULE, ONE OF THESE FORMS COMES TO BE GENERALLY PREFERRED, AND THE LESS CUSTOMARY FORM COMES TO LOOK OBSOLETE AND IS DISCARDED. FROM TIME TO TIME NEW FORMS, MOSTLY SIMPLIFICATIONS, ARE INTRODUCED BY INNOVATORS, AND EITHER WIN THEIR PLACE OR DIE OF NEGLECT.
    End decryption? yes
    """
    # To create a copy of the input string
    encrypted_s_copy = encrypted_s

    # To sort in order of frequency
    valid_coins = get_all_coins(encrypted_s_copy)
    frequencies = get_frequencies(valid_coins)
    frequencies = sort_keys_by_values(frequencies)

    # To create the decryption dictionary 
    decryption_dict = {}
    keys = list(frequencies)
    for i, k in enumerate(keys):
        decryption_dict[k] = get_letter_of_popularity_order(i)
    # To decrypt the string
    decrypted_s = ''
    for coins in valid_coins:
         decrypted_s += decryption_dict[coins]

    # User interaction
    while True:
        print("Decrypted string:", decrypted_s)
        decision = input("End decpryption? ")
        # If the answer is yes
        if decision == 'yes':
            return encrypted_s
        # Swap letters manually 
        else:
            letter1 = input("Enter first letter to swap: ")
            letter2 = input("Enter second letter to swap: ")
            decrypted_s = swap_letters(decrypted_s, letter1, letter2)


if __name__ == '__main__':
    doctest.testmod()

       
  
  
  
    
    
    
    