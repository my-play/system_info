from typing import Dict, Union, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import os
from time import sleep
import time


class GuiTest:
    def __init__(self):
        self.config = get_config()
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(self.config["path_to_Chrome_driver"], options=self.options)
        self.system_information = {}

    def login_page(self):
        self.driver.get(self.config["url"])
        # sleep(2)

    def get_system_os(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['system_os']}", Keys.ENTER))
        sleep(1)
        system_version_raw = self.driver.find_element(By.CSS_SELECTOR,
                                                      '#terminal > div.ace_scroller > div > div.ace_layer.ace_text-layer > div:nth-child(4)')
        system_version = system_version_raw.text
        cut_string = system_version.split('=')
        os_version = cut_string[1]
        self.clear_terminal()
        return os_version

    def get_cpu_name(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['system_cpu']['model_name']}", Keys.ENTER))
        sleep(1)
        cpu_name_raw = self.driver.find_element(By.CSS_SELECTOR,
                                                '#terminal > div.ace_scroller > div > div.ace_layer.ace_text-layer > div:nth-child(3)')
        sleep(1)
        cpu_name = cpu_name_raw.text
        self.clear_terminal()
        return cpu_name

    def get_cpu_vendor_id(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['system_cpu']['vendor_id']}", Keys.ENTER))
        sleep(1)
        cpu_vendor_raw = self.driver.find_element(By.CSS_SELECTOR,
                                                  '#terminal > div.ace_scroller > div > div.ace_layer.ace_text-layer > div:nth-child(3)')
        sleep(1)
        cpu_vendor = cpu_vendor_raw.text
        self.clear_terminal()
        return cpu_vendor

    def get_sata(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['sata']}", Keys.ENTER))
        sleep(1)
        sata_raw = self.driver.find_element(By.CSS_SELECTOR,
                                            '#terminal > div.ace_scroller > div > div.ace_layer.ace_text-layer > div:nth-child(3)')
        sleep(1)
        sata = sata_raw.text
        self.clear_terminal()
        return sata

    def get_pci_list(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['pci_list']}", Keys.ENTER))
        sleep(1)
        pci_list_raw = self.driver.find_element(By.XPATH, '// *[ @ id = "terminal"] / div[2] / div / div[3]')
        before_split = pci_list_raw.text
        splited_list_pci = before_split.split("\n")

        self.clear_terminal()

        return splited_list_pci

    def get_last_login(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['last_login']}", Keys.ENTER))
        sleep(1)

        last_login_raw = self.driver.find_element(By.XPATH, '//*[@id="terminal"]/div[2]/div/div[3]/div[3]')
        last_login = last_login_raw.text

        self.clear_terminal()
        return last_login

    def get_current_time(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['current_time']}", Keys.ENTER))
        sleep(1)

        current_time_raw = self.driver.find_element(By.XPATH, '//*[@id="terminal"]/div[2]/div/div[3]/div[3]')
        current_time = current_time_raw.text

        self.clear_terminal()
        return current_time

    def get_cat_help(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['cat_help']}", Keys.ENTER))
        sleep(1)
        cat_list_raw = self.driver.find_element(By.XPATH, '// *[ @ id = "terminal"] / div[2] / div / div[3]')
        before_split = cat_list_raw.text
        return before_split.split("\n")

    def clear_terminal(self):
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(
            (f"{self.config['system_info']['clear']}", Keys.ENTER))
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//TEXTAREA[@class='ace_text-input']").send_keys(Keys.ENTER)
        sleep(2)


def get_config():
    with open("config.json") as json_file:
        get_config.config = json.load(json_file)
    return get_config.config


gui = GuiTest()
required_system_info = {
    "os_version": gui.get_system_os,
    "cpu_name": gui.get_cpu_name,
    "cpu_vendor": gui.get_cpu_vendor_id,
    "sata_info": gui.get_sata,
    "pci_list": gui.get_pci_list,
    "last_login": gui.get_last_login,
    "current_time": gui.get_current_time,
}


def get_system_info():
    system_info: dict[str, Union[str, list[str]]] = {}
    config = get_config()
    print(f"system config:  {config}")
    gui.login_page()

    for required_info in required_system_info:
        system_info[required_info] = required_system_info[required_info]()

    json_object = json.dumps(system_info, indent=4)
    with open("system_info.json", "w") as outfile:
        outfile.write(json_object)




    # print(os_version, cpu_vendor, cpu_name, sata_info)
