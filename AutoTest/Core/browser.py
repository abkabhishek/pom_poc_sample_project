from selenium import webdriver
import os
import sys




class Browser:
	driver=None

	def __init__(self,browser='chrome'):
		if 'nt' in os.name:			# windows users
			if browser=='chrome':
				print('==============INIT=================')
				driver=webdriver.Chrome(
										executable_path='./Files/drivers/win/chromedriver.exe',
										)
				driver.implicitly_wait(2)
				Browser.driver=driver
				
			else:
				print("Invalid Browser passed")
				
		else:						# linux, mac users
			if browser=='chrome':
				print('==============INIT=================')
				
				# Please make sure to put chromedriver for mac at "usr/local/bin/"
				Browser.driver=webdriver.Chrome()
				
			else:
				print("Invalid Browser passed")