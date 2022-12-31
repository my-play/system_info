import string
import pytest
import re
from GUI_test import GuiTest

cat_command = GuiTest()
cat_command.login_page()
cat_help = cat_command.get_cat_help()
filtered = list(filter(lambda line: re.search('^\s+-[a-zA-Z][,]?\s+', line) != None, cat_help))
options = list(map(lambda line: re.search('^\s+-([a-zA-Z])', line).group(1), filtered))


def get_abc():
    return list(string.ascii_letters)


@pytest.mark.parametrize("letter", get_abc())
def test_cat_command_options(letter):
    assert letter in options, f'cat: invalid option -- {letter} '


