from colorama import Fore as c
import datetime as dt

def color(color='white', obj=dt.datetime.now(), reset=True):
    print(c.__dict__[color.upper()], obj)
    if reset:
        print(c.RESET)

"""
color_codes = {
    'BLACK': '\x1b[30m',
    'BLUE': '\x1b[34m',
    'CYAN': '\x1b[36m',
    'GREEN': '\x1b[32m',
    'LIGHTBLACK_EX': '\x1b[90m',
    'LIGHTBLUE_EX': '\x1b[94m',
    'LIGHTCYAN_EX':'\x1b[96m',
    'LIGHTGREEN_EX': '\x1b[92m',
    'LIGHTMAGENTA_EX': '\x1b[95m',
    'LIGHTRED_EX': '\x1b[91m',
    'LIGHTWHITE_EX': '\x1b[97m',
    'LIGHTYELLOW_EX': '\x1b[93m',
    'MAGENTA': '\x1b[35m',
    'RED': '\x1b[31m',
    'RESET': '\x1b[39m',
    'WHITE': '\x1b[37m',
    'YELLOW': '\x1b[33m'
}
"""
