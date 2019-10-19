"""
This is module to contain commonly used functionality like find elements
"""
import time
from sys import stdout as console

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Com:
    driver = None
    windowTabs = {}

    def __init__(self, driver):
        Com.driver = driver
        
    @classmethod
    def is_exist(cls,locatr):
        return cls.driver.find_elements(*Locatr.get_locatr_by(locatr))
        
    @classmethod
    def get_element_text_else_false(cls,elem):
        if elem:
            return elem.text
        else:
            return False
    
    
        
    @classmethod
    def findElement(cls,locatr,elem=None):
        """
        locatr param should be of "css|string" style
        elem param is optional selenium element, if provided then find_element will be done on that passed element
        """
        if elem:
            return elem.find_element(*Locatr.get_locatr_by(locatr))
        else:
            return cls.driver.find_element(*Locatr.get_locatr_by(locatr))

    @classmethod
    def findElements(cls,locatr,elem=None):
        """
        locatr param should be of "css|string" style
        elem param is optional selenium element, if provided then find_element will be done on that passed element
        """
        if elem:
            return elem.find_elements(*Locatr.get_locatr_by(locatr))
        else:
            return cls.driver.find_elements(*Locatr.get_locatr_by(locatr))


    @classmethod
    def element(cls,locatr):
        """
        This is the custom element function, in every pom class, every locator is created of this type function.
        User can perform action direction on the element, no need to find element first.
        Example:
        
        Home.Search_box().send_keys("search_text")
        
        It can get multiple optional parameters at the time of actions:
        
        Home.Results(True,1).click()  
             => first param = findAll=True - To find list of elements
             => second param = element index to return, else it will return all list.
                        
        """

        def find_element(findAll=False,returnItem=False):
            try:
                if findAll:
                    elems= cls.findElements(locatr)
                else:
                    elem=cls.findElement(locatr)
                
                
                if findAll and returnItem ==False and elems:
                    return elems
                elif findAll and returnItem!=False and elems:
                    return elems[returnItem-1]
                else:
                    return elem
            except Exception as ex:
#                 console.write(str(ex))
                console.write("---- Element not found, Exception occurred while finding the element ----")
                # raise Exception("Element Not found")
                return False
        
        return find_element

    @classmethod
    def elements(cls,locatr):
        """
        This is similar like element function above but its for list of elements specifically
        
        """

        def find_elements(returnItem=False):
            try:
                elems= cls.findElements(locatr)
                
                
                if returnItem == False and elems:
                    return elems
                elif returnItem!=False and elems:
                    return elems[returnItem-1]
                else:
                    return elems
            except Exception as ex:
                # console.write(str(ex))
                console.write("---- Element not found, Exception occurred while finding the elements ----")
#                 raise Exception("Elements Not found")
                return False
        
        return find_elements
    
    # Handling Window tabs
    
    @classmethod
    def add_new_tab(cls,Tab,i):
        cls.windowTabs[Tab]=cls.driver.window_handles[i]
        
    @classmethod
    def switch_to(cls,Tab):
        if Tab in cls.windowTabs:
            cls.driver.switch_to.window(cls.windowTabs[Tab])
            return True
        else:
            console.write("Mentioned Tab name is not present")
            return False
        
    @classmethod
    def close_tab(cls,Tab):
        if cls.switch_to(Tab):
            cls.driver.close()
            del cls.windowTabs[Tab]
        else:
            console.write("Mentioned Tab name is not present")
            return False
        

class Locatr:
    """
    Helper class to convert "css|string" type locator to (CSS_SELECTOR,"string")
    """
    @staticmethod
    def get_locatr_by(locatr):
        
        locatrBy,locatrStr = locatr.split("|")
        
        if locatrBy.lower()=="xpath":
            return By.XPATH,locatrStr
        elif locatrBy.lower()=="id":
            return By.ID,locatrStr
        elif locatrBy.lower()=="css":
            return By.CSS_SELECTOR,locatrStr
        elif locatrBy.lower()=="name":
            return By.NAME,locatrStr
        elif locatrBy.lower()=="class":
            return By.CLASS_NAME,locatrStr
        else:
            return By.ID,locatrStr 


