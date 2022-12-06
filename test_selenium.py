import os
import pytest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.select import Select
from webdriver_manager.firefox import GeckoDriverManager


class TestSelenium:

    def setup_method(self) -> None:
        self.driver = None
        self.url = None
        self.setup_token()
        self.setup_driver()
        self.get_driver()

    def teardown_method(self) -> None:
        self.driver.close()

    def setup_token(self):
        os.environ['GH_TOKEN'] = ""

    def setup_driver(self):
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    def get_driver(self):
        url = "https://www.selenium.dev/selenium/web/web-form.html"
        self.driver.get(url)

    def test_text_input(self):
        test_text = "Selenium"
        text_field = self.driver.find_element(by=By.ID, value="my-text-id")
        text_field.click()
        text_field.send_keys(test_text)
        assert text_field.get_attribute("value") == test_text

    # Check the type property if the input, if it's text the text is not masked, if it's password it is masked.
    def test_password_is_hidden(self):
        test_password = "Selenium2022"
        password_field = self.driver.find_element(by=By.NAME, value="my-password")
        password_field.click()
        password_field.send_keys(test_password)
        assert password_field.get_attribute("type") == "password"

    def test_password(self):
        test_password = "Selenium2022"
        password_field = self.driver.find_element(by=By.NAME, value="my-password")
        password_field.click()
        password_field.send_keys(test_password)
        assert password_field.get_attribute("value") == test_password

    @pytest.mark.parametrize(
        'selection',
        [
            "One",
            "Two",
            "Three"
        ]
    )
    def test_dropdown_selection(self, selection):
        dropdown_element = Select(self.driver.find_element(by=By.NAME, value="my-select"))
        dropdown_element.select_by_visible_text(selection)
        assert dropdown_element.first_selected_option.text == selection

    def test_text_area(self):
        test_text = "Selenium2022"
        text_field = self.driver.find_element(by=By.NAME, value="my-textarea")
        text_field.click()
        text_field.send_keys(test_text)
        assert text_field.get_attribute("value") == test_text

    @pytest.mark.parametrize(
        'selection',
        [
            ("1", "San Francisco"),
            ("2", "New York"),
            ("3", "Seattle"),
            ("4", "Los Angeles"),
            ("5", "Chicago")
        ]
    )
    def test_dropdown_data_list(self, selection):
        data_list_element = self.driver.find_element(by=By.NAME, value="my-datalist")
        data_list_element.click()
        data_list_element.send_keys(selection[1])

        #data_list_field_value = data_list_element.get_attribute("value")
        #assert data_list_field_value == selection[1]

        option_path = "/html/body/main/div/form/div/div[2]/label[2]/datalist/option[{}]".format(selection[0])
        option_element = self.driver.find_element(by=By.XPATH, value=option_path)
        option_value = option_element.get_attribute("value")
        assert option_value == selection[1]

    def test_checked_checkbox_is_checked(self):
        checkbox_element = self.driver.find_element(by=By.ID, value="my-check-1")
        assert checkbox_element.is_selected()

    def test_checked_checkbox_is_unchecked_after_select(self):
        checkbox_element = self.driver.find_element(by=By.ID, value="my-check-1")
        checkbox_element.click()
        assert checkbox_element.is_selected() is False

    def test_default_checkbox_is_unchecked(self):
        checkbox_element = self.driver.find_element(by=By.ID, value="my-check-2")
        assert checkbox_element.is_selected() is False

    def test_default_checkbox_is_checked_after_select(self):
        checkbox_element = self.driver.find_element(by=By.ID, value="my-check-2")
        checkbox_element.click()
        assert checkbox_element.is_selected()

    def test_default_radio_is_not_selected(self):
        radio_element = self.driver.find_element(by=By.ID, value="my-radio-2")
        assert radio_element.is_selected() is False

    def test_default_radio_is_selected_after_select(self):
        radio_element = self.driver.find_element(by=By.ID, value="my-radio-2")
        radio_element.click()
        assert radio_element.is_selected()

    def test_selected_radio_is_selected(self):
        radio_element = self.driver.find_element(by=By.ID, value="my-radio-1")
        assert radio_element.is_selected()
