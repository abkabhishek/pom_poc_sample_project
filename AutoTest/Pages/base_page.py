"""
This is Common page to handle common elements across the pages.
"""
import time
from sys import stdout as console

from Core.com import *



class BasePage(object):
    driver = None

    def __init__(self,driver):
        BasePage.driver = driver
        self.com = Com(driver)
        
    def close(self):
        BasePage.driver.close()
        
    def quit(self):
        BasePage.driver.quit()