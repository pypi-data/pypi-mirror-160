"""
Colorway
https://github.com/xhelphin/colorway

Python package to change the text color of the python console.

Foreground package
"""

# Import and call os.system to initialise color support on windows
from multiprocessing.sharedctypes import Value
import os
if os.name == 'nt':
    os.system("")

def black_fg(string):
    """
    Return a formatted string with a black foreground
    """
    return f"\033[0;30m{string}\033[0m"

def red_fg(string):
    """
    Return a formatted string with a red foreground
    """
    return f"\033[0;31m{string}\033[0m"

def green_fg(string):
    """
    Return a formatted string with a green foreground
    """
    return f"\033[0;32m{string}\033[0m"

def yellow_fg(string):
    """
    Return a formatted string with a yellow foreground
    """
    return f"\033[0;33m{string}\033[0m"

def blue_fg(string):
    """
    Return a formatted string with a blue foreground
    """
    return f"\033[0;34m{string}\033[0m"

def purple_fg(string):
    """
    Return a formatted string with a purple foreground
    """
    return f"\033[0;35m{string}\033[0m"

def cyan_fg(string):
    """
    Return a formatted string with a cyan foreground
    """
    return f"\033[0;36m{string}\033[0m"

def white_fg(string):
    """
    Return a formatted string with a white foreground
    """
    return f"\033[0;37m{string}\033[0m"

def bold_black_fg(string):
    """
    Return a formatted string with a bold black foreground
    """
    return f"\033[1;30m{string}\033[0m"

def bold_red_fg(string):
    """
    Return a formatted string with a bold red foreground
    """
    return f"\033[1;31m{string}\033[0m"

def bold_green_fg(string):
    """
    Return a formatted string with a bold green foreground
    """
    return f"\033[1;32m{string}\033[0m"

def bold_yellow_fg(string):
    """
    Return a formatted string with a bold yellow foreground
    """
    return f"\033[1;33m{string}\033[0m"

def bold_blue_fg(string):
    """
    Return a formatted string with a bold blue foreground
    """
    return f"\033[1;34m{string}\033[0m"

def bold_purple_fg(string):
    """
    Return a formatted string with a bold purple foreground
    """
    return f"\033[1;35m{string}\033[0m"

def bold_cyan_fg(string):
    """
    Return a formatted string with a bold cyan foreground
    """
    return f"\033[1;36m{string}\033[0m"

def bold_white_fg(string):
    """
    Return a formatted string with a bold white foreground
    """
    return f"\033[1;37m{string}\033[0m"

def underline_black_fg(string):
    """
    Return a formatted string with an underlined black foreground
    """
    return f"\033[4;30m{string}\033[0m"

def underline_red_fg(string):
    """
    Return a formatted string with an underlined red foreground
    """
    return f"\033[4;31m{string}\033[0m"

def underline_green_fg(string):
    """
    Return a formatted string with an underlined green foreground
    """
    return f"\033[4;32m{string}\033[0m"

def underline_yellow_fg(string):
    """
    Return a formatted string with an underlined yellow foreground
    """
    return f"\033[4;33m{string}\033[0m"

def underline_blue_fg(string):
    """
    Return a formatted string with an underlined blue foreground
    """
    return f"\033[4;34m{string}\033[0m"

def underline_purple_fg(string):
    """
    Return a formatted string with an underlined purple foreground
    """
    return f"\033[4;35m{string}\033[0m"

def underline_cyan_fg(string):
    """
    Return a formatted string with an underlined cyan foreground
    """
    return f"\033[4;36m{string}\033[0m"

def underline_white_fg(string):
    """
    Return a formatted string with an underlined white foreground
    """
    return f"\033[4;37m{string}\033[0m"

def highintensity_black_fg(string):
    """
    Return a formatted string with a high-intensity black foreground
    """
    return f"\033[0;90m{string}\033[0m"

def highintensity_red_fg(string):
    """
    Return a formatted string with a high-intensity red foreground
    """
    return f"\033[0;91m{string}\033[0m"

def highintensity_green_fg(string):
    """
    Return a formatted string with a high-intensity green foreground
    """
    return f"\033[0;92m{string}\033[0m"

def highintensity_yellow_fg(string):
    """
    Return a formatted string with a high-intensity yellow foreground
    """
    return f"\033[0;93m{string}\033[0m"

def highintensity_blue_fg(string):
    """
    Return a formatted string with a high-intensity blue foreground
    """
    return f"\033[0;94m{string}\033[0m"

def highintensity_purple_fg(string):
    """
    Return a formatted string with a high-intensity purple foreground
    """
    return f"\033[0;95m{string}\033[0m"

def highintensity_cyan_fg(string):
    """
    Return a formatted string with a high-intensity cyan foreground
    """
    return f"\033[0;96m{string}\033[0m"

def highintensity_white_fg(string):
    """
    Return a formatted string with a high-intensity white foreground
    """
    return f"\033[0;97m{string}\033[0m"

def highintensity_bold_black_fg(string):
    """
    Return a formatted string with a bold high-intensity black foreground
    """
    return f"\033[1;90m{string}\033[0m"

def highintensity_bold_red_fg(string):
    """
    Return a formatted string with a bold high-intensity red foreground
    """
    return f"\033[1;91m{string}\033[0m"

def highintensity_bold_green_fg(string):
    """
    Return a formatted string with a bold high-intensity green foreground
    """
    return f"\033[1;92m{string}\033[0m"

def highintensity_bold_yellow_fg(string):
    """
    Return a formatted string with a bold high-intensity yellow foreground
    """
    return f"\033[1;93m{string}\033[0m"

def highintensity_bold_blue_fg(string):
    """
    Return a formatted string with a bold high-intensity blue foreground
    """
    return f"\033[1;94m{string}\033[0m"

def highintensity_bold_purple_fg(string):
    """
    Return a formatted string with a bold high-intensity purple foreground
    """
    return f"\033[1;95m{string}\033[0m"

def highintensity_bold_cyan_fg(string):
    """
    Return a formatted string with a bold high-intensity cyan foreground
    """
    return f"\033[1;96m{string}\033[0m"

def highintensity_bold_white_fg(string):
    """
    Return a formatted string with a bold high-intensity white foreground
    """
    return f"\033[1;97m{string}\033[0m"

def custom_fg(red, green, blue, string):
    """
    Return a formatted string with a custom colored foreground
    Arguments:
    - red -> integer 0 to 255
    - green -> integer 0 to 255
    - blue -> integer 0 to 255
    - string -> string to format
    """
    try:
        red = int(red)
        green = int(green)
        blue = int(blue)
        if red < 0 or red > 255:
            raise ValueError
        if green < 0 or green > 255:
            raise ValueError
        if blue < 0 or blue > 255:
            raise ValueError
    except ValueError:
        print("Colorways: Arguments red, green & blue need to be integers between 0 and 255.")
    else:
        return f"\033[38;2;{red};{green};{blue}m{string}\033[0m"