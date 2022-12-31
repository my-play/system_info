import pytest
from GUI_test import GuiTest

gui_obj = GuiTest()
@pytest.fixture(scope="session")
def login_page():
    page=gui_obj.login_page()
    return page
