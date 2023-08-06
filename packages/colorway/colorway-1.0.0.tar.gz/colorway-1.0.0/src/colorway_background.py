"""
Colorway
https://github.com/xhelphin/colorway

Python package to change the text color of the python console.

Foreground package
"""

# Import and call os.system to initialise color support on windows
import os
if os.name == 'nt':
    os.system("")

def black_bg(string):
    """
    Return a formatted string with a black background
    """
    return f"\033[40m{string}\033[0m"

def red_bg(string):
    """
    Return a formatted string with a red background
    """
    return f"\033[41m{string}\033[0m"

def green_bg(string):
    """
    Return a formatted string with a green background
    """
    return f"\033[42m{string}\033[0m"

def yellow_bg(string):
    """
    Return a formatted string with a yellow background
    """
    return f"\033[43m{string}\033[0m"

def blue_bg(string):
    """
    Return a formatted string with a blue background
    """
    return f"\033[44m{string}\033[0m"

def purple_bg(string):
    """
    Return a formatted string with a purple background
    """
    return f"\033[45m{string}\033[0m"

def cyan_bg(string):
    """
    Return a formatted string with a cyan background
    """
    return f"\033[46m{string}\033[0m"

def white_bg(string):
    """
    Return a formatted string with a white background
    """
    return f"\033[47m{string}\033[0m"

def highintensity_black_bg(string):
    """
    Return a formatted string with a high-intensity black background
    """
    return f"\033[0;100m{string}\033[0m"

def highintensity_red_bg(string):
    """
    Return a formatted string with a high-intensity red background
    """
    return f"\033[0;101m{string}\033[0m"

def highintensity_green_bg(string):
    """
    Return a formatted string with a high-intensity green background
    """
    return f"\033[0;102m{string}\033[0m"

def highintensity_yellow_bg(string):
    """
    Return a formatted string with a high-intensity yellow background
    """
    return f"\033[0;103m{string}\033[0m"

def highintensity_blue_bg(string):
    """
    Return a formatted string with a high-intensity blue background
    """
    return f"\033[0;104m{string}\033[0m"

def highintensity_purple_bg(string):
    """
    Return a formatted string with a high-intensity purple background
    """
    return f"\033[0;105m{string}\033[0m"

def highintensity_cyan_bg(string):
    """
    Return a formatted string with a high-intensity cyan background
    """
    return f"\033[0;106m{string}\033[0m"

def highintensity_white_bg(string):
    """
    Return a formatted string with a high-intensity white background
    """
    return f"\033[0;107m{string}\033[0m"

def custom_bg(red, green, blue, string):
    """
    Return a formatted string with a custom colored background
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
        return f"\033[48;2;{red};{green};{blue}m{string}\033[0m"