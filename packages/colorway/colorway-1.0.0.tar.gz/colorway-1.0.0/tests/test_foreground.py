from colorway_foreground import *

def test_black():
    assert black_fg("test") == '\x1b[0;30mtest\x1b[0m'

def test_red():
    assert red_fg("test") == '\x1b[0;31mtest\x1b[0m'

def test_green():
    assert green_fg("test") == '\x1b[0;32mtest\x1b[0m'

def test_yellow():
    assert yellow_fg("test") == '\x1b[0;33mtest\x1b[0m'

def test_blue():
    assert blue_fg("test") == '\x1b[0;34mtest\x1b[0m'

def test_purple():
    assert purple_fg("test") == '\x1b[0;35mtest\x1b[0m'

def test_cyan():
    assert cyan_fg("test") == '\x1b[0;36mtest\x1b[0m'

def test_white():
    assert white_fg("test") == '\x1b[0;37mtest\x1b[0m'

def test_bold_black():
    assert bold_black_fg("test") == '\x1b[1;30mtest\x1b[0m'

def test_bold_red():
    assert bold_red_fg("test") == '\x1b[1;31mtest\x1b[0m'

def test_bold_green():
    assert bold_green_fg("test") == '\x1b[1;32mtest\x1b[0m'

def test_bold_yellow():
    assert bold_yellow_fg("test") == '\x1b[1;33mtest\x1b[0m'

def test_bold_blue():
    assert bold_blue_fg("test") == '\x1b[1;34mtest\x1b[0m'

def test_bold_purple():
    assert bold_purple_fg("test") == '\x1b[1;35mtest\x1b[0m'

def test_bold_cyan():
    assert bold_cyan_fg("test") == '\x1b[1;36mtest\x1b[0m'

def test_bold_white():
    assert bold_white_fg("test") == '\x1b[1;37mtest\x1b[0m'

def test_underline_black():
    assert underline_black_fg("test") == '\x1b[4;30mtest\x1b[0m'

def test_underline_red():
    assert underline_red_fg("test") == '\x1b[4;31mtest\x1b[0m'

def test_underline_green():
    assert underline_green_fg("test") == '\x1b[4;32mtest\x1b[0m'

def test_underline_yellow():
    assert underline_yellow_fg("test") == '\x1b[4;33mtest\x1b[0m'

def test_underline_blue():
    assert underline_blue_fg("test") == '\x1b[4;34mtest\x1b[0m'

def test_underline_purple():
    assert underline_purple_fg("test") == '\x1b[4;35mtest\x1b[0m'

def test_underline_cyan():
    assert underline_cyan_fg("test") == '\x1b[4;36mtest\x1b[0m'

def test_underline_white():
    assert underline_white_fg("test") == '\x1b[4;37mtest\x1b[0m'

def test_highintensity_black():
    assert highintensity_black_fg("test") == '\x1b[0;90mtest\x1b[0m'

def test_highintensity_red():
    assert highintensity_red_fg("test") == '\x1b[0;91mtest\x1b[0m'

def test_highintensity_green():
    assert highintensity_green_fg("test") == '\x1b[0;92mtest\x1b[0m'

def test_highintensity_yellow():
    assert highintensity_yellow_fg("test") == '\x1b[0;93mtest\x1b[0m'

def test_highintensity_blue():
    assert highintensity_blue_fg("test") == '\x1b[0;94mtest\x1b[0m'

def test_highintensity_purple():
    assert highintensity_purple_fg("test") == '\x1b[0;95mtest\x1b[0m'

def test_highintensity_cyan():
    assert highintensity_cyan_fg("test") == '\x1b[0;96mtest\x1b[0m'

def test_highintensity_white():
    assert highintensity_white_fg("test") == '\x1b[0;97mtest\x1b[0m'

def test_highintensity_bold_black():
    assert highintensity_bold_black_fg("test") == '\x1b[1;90mtest\x1b[0m'

def test_highintensity_bold_red():
    assert highintensity_bold_red_fg("test") == '\x1b[1;91mtest\x1b[0m'

def test_highintensity_bold_green():
    assert highintensity_bold_green_fg("test") == '\x1b[1;92mtest\x1b[0m'

def test_highintensity_bold_yellow():
    assert highintensity_bold_yellow_fg("test") == '\x1b[1;93mtest\x1b[0m'

def test_highintensity_bold_blue():
    assert highintensity_bold_blue_fg("test") == '\x1b[1;94mtest\x1b[0m'

def test_highintensity_bold_purple():
    assert highintensity_bold_purple_fg("test") == '\x1b[1;95mtest\x1b[0m'

def test_highintensity_bold_cyan():
    assert highintensity_bold_cyan_fg("test") == '\x1b[1;96mtest\x1b[0m'

def test_highintensity_bold_white():
    assert highintensity_bold_white_fg("test") == '\x1b[1;97mtest\x1b[0m'

def test_custom():
    assert custom_fg(1,2,3,"test") == '\x1b[38;2;1;2;3mtest\x1b[0m'