
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

TERMINAL_CODES = {
    '0': '\x1b[30m',
    '1': '\x1b[34m',
    '2': '\x1b[32m',
    '3': '\x1b[36m',
    '4': '\x1b[31m',
    '5': '\x1b[35m',
    '6': '\x1b[33m',
    '7': '\x1b[37m',
    '8': '\x1b[90m',
    '9': '\x1b[94m',
    'a': '\x1b[92m',
    'b': '\x1b[96m',
    'c': '\x1b[91m',
    'd': '\x1b[95m',
    'e': '\x1b[93m',
    'f': '\x1b[97m',
    'k': '\x1b[5m',  # Code for "slow blink" which is close enough to Minecraft's obfuscated style
    'l': '\x1b[1m',
    'm': '\x1b[9m',
    'n': '\x1b[4m',
    'o': '\x1b[3m',
    'r': '\x1b[0m'
}
