"""
Hotel Results page Pom and its locator class
"""
import time
from sys import stdout as console

from Pages.base_page import BasePage
    
    
    
class HotelResultsLocators:
    """Hotel Results Page Locators"""

    LocatersList = {
    'hotel_results_list' : 'css|#hotellist_inner>div[class*="sr_item"]',
    'hotel_results_name_list':'css|#hotellist_inner>div[class*="sr_item"] a[class*="hotel_name_link"] span.sr-hotel__name',
    'pagination_list':'css|nav[class*=pagination__nav] ul ul[class*=pagination__list] li',
    'pagination_previous_page':'css|nav[class*=pagination__nav] ul[class*=pagination__list]>li[class*=pagination__prev]',
    'pagination_next_page':'css|nav[class*=pagination__nav] ul[class*=pagination__list]>li[class*=pagination__next]',
    'checkin_calendar_overlay_close_button':'css|div.c2-calendar button[class*=close]'
    }
    
class HotelResultsPage(BasePage):

    def __init__(self,driver):
        super(HotelResultsPage,self).__init__(driver)
        
        # Below is creating class attribute for each locator in Locator class as one Element object and one locator_* string
        for k,v in HotelResultsLocators.LocatersList.items():
            setattr(self,k,self.com.element(v))
            setattr(self,"locator_"+k,v)
            
    def is_checkin_calendar_over_appearing(self):
        return self.checkin_calendar_overlay_close_button().is_displayed()
    
    
    def click_checkin_calendar_over_close_button(self):
        self.checkin_calendar_overlay_close_button().click()


    def hide_all_auto_overlay_if_any(self,exceptThese=[]):
        """
        To implement overlay hide for different overlay, 
        
        """
        
        #checkin calendar overaly
        if "checkin" not in exceptThese:
            if self.is_checkin_calendar_over_appearing():
                self.click_checkin_calendar_over_close_button()

            
    def check_results_available(self):
        return len(self.hotel_results_list(findAll=True))
    
    def is_specific_hotel_name_present(self,hotel_name,case_sensitive=False):
        if self.check_results_available():
            count =0
            hotel_name_element = self.hotel_results_name_list(findAll=True)
            
            for name_elem in hotel_name_element:
                count+=1
                if case_sensitive:
                    if hotel_name in name_elem.text:
                        return count
                else:
                    if hotel_name.lower() in name_elem.text.lower():
                        return count
            message = "Hotel name {} not found in results on the page".format(hotel_name)
            return False, message
        else:
            message = "No results found"
            return False, message
            
    def click_nth_hotel_result(self,nth):
        self.hotel_results_name_list(True,nth).click()
        time.sleep(1)
        self.com.add_new_tab("HotelResultsPage",0)
        self.com.add_new_tab("HotelDetailPage",1)
        return True
        
    def click_on_nth_page(self,nth):
        """ Paginations methods """
        paginations = self.pagination_list(True)
        if len(paginations)>=nth:
            paginations[nth-1].click()
            return True
        else:
            message="nth-{} value is greater than paginations-{}".format(nth, len(paginations))
            return False,message
        
        
    def click_on_next_page(self):
        """ Paginations methods """
        if "disabled" in self.pagination_next_page().get_attribute("class"):
            message = "Next page button is disabled"
            return False,message
        else:
            self.pagination_next_page().click()
            return True
        
    
    def click_on_previous_page(self):
        """ Paginations methods """
        if "disabled" in self.pagination_previous_page().get_attribute("class"):
            message = "Previous page button is disabled"
            return False,message
        else:
            self.pagination_previous_page().click()
            return True
        
        
        