"""
Hotel page Pom and its locator class
"""
import time
from sys import stdout as console

from Pages.base_page import BasePage


class HomeLocators:
    """Home Page Locators"""

    LocatersList = {
    'search_box' : 'id|ss',
    'search_button':'css|button[class*="sb-searchbox__button"]'
    }


class HomePage(BasePage):
    """ Home Page Class """

    def __init__(self,driver,homeurl=None):
        super(HomePage,self).__init__(driver)
        self.homeurl=homeurl
        
        # Below is creating class attribute for each locator in Locator class as one Element object and one locator_* string
        for k,v in HomeLocators.LocatersList.items():
            setattr(self,k,self.com.element(v))
            setattr(self,"locator_"+k,v)
        
        
    def open_home_page(self,url=None):
        if url:
            self.driver.get(url)   
        else:
            self.driver.get(self.homeurl) 
        
    # Search Methods 
    def input_search_string(self,search_string):
        self.search_box().send_keys(search_string)
        time.sleep(5)
        
        
    def click_search_button(self):
        self.search_button().click()
        
        
    def perform_search(self,search_string,dates=None,persons=None):
        
        self.input_search_string(search_string)
        
        if dates:
            pass   #TBD
        
        if persons:
            pass   #TBD
        
        self.click_search_button()
        
        