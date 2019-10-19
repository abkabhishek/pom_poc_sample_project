"""
Hotel Detail page Pom and its locator class
"""
import time
from sys import stdout as console

from Pages.base_page import BasePage


    
    
class HotelDetailPageLocators:
    """Hotel Detail Page Locators"""

    LocatersList = {
    'hotel_name' : 'id|hp_hotel_name',
    'hotel_type_badge':'css|#hp_hotel_name>span',
    'hotel_star_rating':'css|span[class*="hp__hotel_ratings__stars"] span',
    'hotel_address':'css|span[class*="hp_address_subtitle"]',
    'occupancy_list':'css|.occ_no_dates',
    'checkin_calendar_overlay_close_button':'css|div.c2-calendar button[class*=close]',
    'occupancy_row_list':'css|tbody td.occ_no_dates',
    'occupancy_adults_subelemnt_list':'css|span.occupancy_adults>i',
    'occupancy_children_subelemnt_list':'css|span.occupancy_children>i',
    'occupancy_adults_list':'css|.occ_no_dates:nth-child(1) span.occupancy_adults',
    'occupancy_children_list':'css|.occ_no_dates:nth-child(1) span.occupancy_children',
    'checkin_checkout_time_list':'css|p span.u-display-block',
    'services_title_list':'xpath|//span[@class="facilityGroupIcon"]/../../h5',
    'services_text_list':'xpath|//span[@class="facilityGroupIcon"]/../../ul'
    }


class HotelDetailPage(BasePage):

    def __init__(self,driver):
        super(HotelDetailPage,self).__init__(driver)
        
        
        # Below is creating class attribute for each locator in Locator class as one Element object and one locator_* string
        for k,v in HotelDetailPageLocators.LocatersList.items():
            setattr(self,k,self.com.element(v))
            setattr(self,"locator_"+k,v)
            
    
    def get_hotel_name(self):
        return self.com.get_element_text_else_false(self.hotel_name())

    def get_hotel_badge(self):
        return self.com.get_element_text_else_false(self.hotel_type_badge())
        
    def get_hotel_star_rating(self):
        return self.com.get_element_text_else_false(self.hotel_star_rating())
        
    def get_hotel_address_string(self):
        return self.com.get_element_text_else_false(self.hotel_address())
        
                    
    def get_full_occupancy_list(self):
        """ To get list of full occupancy count list as per available rooms in a format : [Total, Adults, childern]"""
        
        occupancyRows = self.occupancy_row_list(True)
        if occupancyRows:
            OccupancyList =[]
            for item in occupancyRows:
                Adults = self.com.findElements(self.locator_occupancy_adults_subelemnt_list,item)
                Children = self.com.findElements(self.locator_occupancy_children_subelemnt_list,item)
                OccupancyList.append([len(Adults)+len(Children),len(Adults),len(Children)])
            return OccupancyList
        else:
            console.write("Occupancy list not found")
            return False
        
        
    def get_max_occupancy(self,otype="all"):
        full_occupancy = self.get_full_occupancy_list()
        if otype=="adults":
            i = 1
        elif otype=="children":
            i = 2
        else:
            i=0
        max = 0
        for item in full_occupancy:
            if max<item[i]:
                max=item[i]
        return max
    
    def is_x_occupancy_available(self,x,otype="all"):
        full_occupancy = self.get_full_occupancy_list()
        if otype=="adults":
            i = 1
        elif otype=="children":
            i = 2
        else:
            i=0
        max = 0
        for item in full_occupancy:
            if x==item[i]:
                return True
        return False
    
    def get_checkin_checkout_time_string(self):
        checkin_time,checkout_time = self.checkin_checkout_time_list(True)
        checkin_time,checkout_time = checkin_time.get_attribute("data-from"),checkout_time.get_attribute("data-until")
        
        return checkin_time,checkout_time
    
    def check_checkin_checkout_time(self,checkin_hrs_str, checkout_hrs_str):
        checkin_actual_str,checkout_actual_str = self.get_checkin_checkout_time_string()
        checkin_actual,checkout_actual = int(checkin_actual_str.replace(":","")),int(checkout_actual_str.replace(":",""))
        checkin_expected,checkout_expected = int(checkin_hrs_str.replace(":","")),int(checkout_hrs_str.replace(":",""))
        CheckResults =[]
        if checkin_expected>=checkin_actual:
            CheckResults.append(True)
        else:
            CheckResults.append(False)
        if checkout_expected<=checkout_actual:
            CheckResults.append(True)
        else:
            CheckResults.append(False)
        return CheckResults
        
        
    def get_available_service_titles(self):
        ListOfServices = []
        los = self.services_title_list(True)
        if los:
            for item in los:
                ListOfServices.append(item.text)
        else:
            console.write("List of Services not found")
            return False
        return ListOfServices
    
    def get_available_service_texts(self):
        """ To get text of available services.
            Except last one as html structure is different.
        """
        ListOfServicesT = []
        los = self.services_text_list(True)
        if los:
            for item in los:
                ListOfServicesT.append(item.text)
        else:
            console.write("List of Services not found")
            return False
        return ListOfServicesT

    def check_free_wifi(self):
        ServicesTitles = self.get_available_service_titles()
        ServicesText = self.get_available_service_texts()
        
        for i in range(len(ServicesText)):
            if "internet" in ServicesTitles[i].lower():
                if "free" in ServicesText[i].lower():
                    return True
                else:
                    return False
        console.write("Internet service not found")
        return False
            