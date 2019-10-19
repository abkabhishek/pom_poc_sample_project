import time
import sys
import pytest
from sys import stdout as console
sys.path.append('.')


from Core.browser import Browser
from Pages.base_page import BasePage
from Pages.home_page import HomePage
from Pages.hotel_search_results_page import HotelResultsPage
from Pages.hotel_detail_page import HotelDetailPage
from TestData.testreader import get_hotel_list


# TestData = [
#     ("Hotel Boss","Rusia"),
#     ("Hotel Minsk","Belarus")
#     ]

TestData = get_hotel_list()

# run by :  python -m pytest Tests/Test_sample.py -v
#or
# run by :  pytest -s Tests/Test_sample.py -v


class Page:

    def __init__(self,driver,url):
        self.Home = HomePage(driver,url)
        self.HotelResults = HotelResultsPage(driver)
        self.Hoteldetailpage =HotelDetailPage(driver)




class TestUM:

    def setup(self):
        B = Browser()
        self.page = Page(B.driver,"https://www.booking.com/")

    def teardown(self):
        self.page.Home.quit()


    @pytest.mark.parametrize("Hotel",TestData)
    def test_verify_search_hotel_basic_info(self,Hotel):
        
        self.page.Home.open_home_page("https://www.booking.com/")
        
        self.page.Home.perform_search(Hotel["hotel_search_string"])
        
        time.sleep(2)
        
        self.page.HotelResults.hide_all_auto_overlay_if_any()        
        
        foundhotel=self.page.HotelResults.is_specific_hotel_name_present(Hotel["hotel_name"])
        
        # Verify if desired hotel present in the results.
        console.write("\nverify if desired hotel present in the results: {}\n".format(foundhotel))
        pytest.assume(bool(foundhotel)==True)
        

        self.page.HotelResults.click_nth_hotel_result(foundhotel)        
        self.page.HotelResults.com.switch_to("HotelDetailPage")
        
        
        # Verify Hotel star rating
        expectedRating=Hotel["star_rating"]
        ratings = self.page.Hoteldetailpage.get_hotel_star_rating()
        console.write("verify hotel star ratings is {} star, actual:{}\n".format(expectedRating,ratings))
        if ratings:
            pytest.assume(expectedRating in ratings)
        else:
            pytest.assume(ratings)
            console.write("Hotel star ratings is not available\n")
        
        
        # Verify Hotel location
        expectedLocation = Hotel["hotel_location"].lower()
        full_address_string = self.page.Hoteldetailpage.get_hotel_address_string().lower()
        console.write("verify if hotel is located in {}, actual address:{}\n".format(expectedLocation,full_address_string))
        if full_address_string:
            pytest.assume(expectedLocation in full_address_string)
        else:
            pytest.assume(full_address_string)
            console.write("Hotel address is not available \n")
        
        
        # Verify if Wifi is available
        expectedWifi = bool(Hotel["free_wifi_available"])
        wifi = self.page.Hoteldetailpage.check_free_wifi()
        console.write("verify if wifi is available:{}, expected: {} \n".format(wifi,expectedWifi))
        pytest.assume(wifi==expectedWifi)
        
        
        
        # Verify if checkin and checkout time.
        expected_checkin_time=Hotel["checkin_time"]
        expected_checkout_time=Hotel["checkout_time"]
        check_in_out = self.page.Hoteldetailpage.check_checkin_checkout_time(expected_checkin_time,expected_checkout_time)
        
        console.write("verify check in time:{} is available : {}\n".format(expected_checkin_time,check_in_out[0]))
        pytest.assume(check_in_out[0]==True)
        
        console.write("verify check out time:{} is available : {}\n".format(expected_checkout_time,check_in_out[1]))
        pytest.assume(check_in_out[1]==True)
        
        
        
        # Verify Hotel's occupancy required
        expectedOccupancy = Hotel["occupancy_required"]   # We are taking it as Adults
        result = self.page.Hoteldetailpage.is_x_occupancy_available(expectedOccupancy, "adults")
        console.write("verify if Hotel have required occupancy of {} available:{}\n".format(expectedOccupancy,result))
        pytest.assume(result)
        
        
        # Verify Hotel's occupancy not required
        NotexpectedOccupancy = Hotel["occupancy_not_required"]   # We are taking it as Adults
        result = self.page.Hoteldetailpage.is_x_occupancy_available(NotexpectedOccupancy, "adults")
        console.write("verify if Hotel have not required occupancy of {} available:{}\n".format(NotexpectedOccupancy,result))
        pytest.assume(result==False)
        