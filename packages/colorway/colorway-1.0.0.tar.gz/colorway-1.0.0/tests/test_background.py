from colorway_background import *

def test_black():
    assert black_bg("test") == '\x1b[40mtest\x1b[0m'

def test_red():
    assert red_bg("test") == '\x1b[41mtest\x1b[0m'

def test_green():
    assert green_bg("test") == '\x1b[42mtest\x1b[0m'

def test_yellow():
    assert yellow_bg("test") == '\x1b[43mtest\x1b[0m'

def test_blue():
    assert blue_bg("test") == '\x1b[44mtest\x1b[0m'

def test_purple():
    assert purple_bg("test") == '\x1b[45mtest\x1b[0m'

def test_cyan():
    assert cyan_bg("test") == '\x1b[46mtest\x1b[0m'

def test_white():
    assert white_bg("test") == '\x1b[47mtest\x1b[0m'

def test_highintensity_black():
    assert highintensity_black_bg("test") == '\x1b[0;100mtest\x1b[0m'

def test_highintensity_red():
    assert highintensity_red_bg("test") == '\x1b[0;101mtest\x1b[0m'

def test_highintensity_green():
    assert highintensity_green_bg("test") == '\x1b[0;102mtest\x1b[0m'

def test_highintensity_yellow():
    assert highintensity_yellow_bg("test") == '\x1b[0;103mtest\x1b[0m'

def test_highintensity_blue():
    assert highintensity_blue_bg("test") == '\x1b[0;104mtest\x1b[0m'

def test_highintensity_purple():
    assert highintensity_purple_bg("test") == '\x1b[0;105mtest\x1b[0m'

def test_highintensity_cyan():
    assert highintensity_cyan_bg("test") == '\x1b[0;106mtest\x1b[0m'

def test_highintensity_white():
    assert highintensity_white_bg("test") == '\x1b[0;107mtest\x1b[0m'

def test_custom():
    assert custom_bg(1,2,3,"test") == '\x1b[48;2;1;2;3mtest\x1b[0m'