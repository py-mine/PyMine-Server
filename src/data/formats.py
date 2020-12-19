
__all__ = (FORMAT_BY_CODE, FORMAT_BY_NAME, FORMATS_COMBINED)

FORMAT_BY_CODE = {
    '0': 'black',
    '1': 'dark_blue',
    '2': 'dark_green',
    '3': 'dark_aqua',
    '4': 'dark_red',
    '5': 'dark_purple',
    '6': 'gold',
    '7': 'gray',
    '8': 'dark_gray',
    '9': 'blue',
    'a': 'green',
    'b': 'aqua',
    'c': 'red',
    'd': 'light_purple',
    'e': 'yellow',
    'f': 'white',
    'k': 'obfuscated',
    'l': 'bold',
    'm': 'strikethrough',
    'n': 'underlined',
    'o': 'italic',
    'r': 'reset'
}

FORMAT_BY_NAME = {v, k for k, v in FORMAT_BY_CODE.items()}

FORMATS_COMBINED = {f'§{code}' for code in list(FORMAT_BY_CODE)}
