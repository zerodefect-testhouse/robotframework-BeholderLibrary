
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import requests
from typing import Optional
import os

class BeholderLibrary(object):

	def __init__(self):
		
		self.original_style = None
		self.beholder_url = 'http://177.136.76.173:8881'
		# self.beholder_url = 'http://127.0.0.1:8000'
		self.selib = BuiltIn().get_library_instance('SeleniumLibrary')
		self.build_number = None

	def get_driver(self):
		return self.selib.driver

	def start_build(self):
		print ("######## START BUILD")
		self.build_number = BuiltIn().get_variable_value("${BEHOLDER_BUILD_NUMBER}")
		
		if self.build_number is None:
			print ("######## BUILD_NUMBER IS NONE")
			payload = {
				"token": os.environ["BEHOLDER_TOKEN"],
				"build_number": "None"
			}
			print ("######## SEND REQUEST TO GET BUILD_NUMBER")
			response = requests.post(f"{self.beholder_url}/api/v1/start_project_build/", data=payload)
			if not response.ok:
				raise PermissionError(response.json()['error'])
			self.build_number = response.json()["build_number"]
			BuiltIn().set_global_variable('${BEHOLDER_BUILD_NUMBER}', self.build_number)

	def upload_snapshot(self, test_name, snapshot):
		print ("######## START UPLOAD SNAPSHOT")
		payload = payload = {
				"token": os.environ['BEHOLDER_TOKEN'],
				"build_number": self.build_number,
				"test_name": test_name
			}

		print ("######## ATTACH FILES")
		files = {
			"snapshot_image": ("snapshot_image.png", snapshot,"image/png"),
			}
		print ("######## SEND REQUEST TO UPLOAD SNAPSHOT")
		response = requests.post(f"{self.beholder_url}/api/v1/upload_snapshot/", data=payload, files=files)
		if not response.ok:
			raise PermissionError(response.json()['error'])

	def capture_snapshot(self, test_name, custom_css=None):
		self.driver = self.get_driver()
		self.start_build()
		scroll_height = self.driver.execute_script('return document.documentElement.scrollHeight')
		original_size = self.driver.get_window_size()
		self.driver.set_window_size(1280, scroll_height)

		if custom_css is not None:
			self.add_custom_css(custom_css=custom_css)

		snapshot = self.driver.get_screenshot_as_png()
		self.upload_snapshot(test_name=test_name, snapshot=snapshot)

		if custom_css is not None:
			self.reset_css()
		self.driver.set_window_size(original_size['width'], original_size['height'])

	def capture_element_snapshot(self, locator, test_name, custom_css=None):
		self.driver = self.get_driver()
		self.start_build()
		
		# scroll_height = self.driver.execute_script('return document.documentElement.scrollHeight')
		# original_size = self.driver.get_window_size()
		# self.driver.set_window_size(1280, scroll_height)

		element = self.selib.find_element(locator)
		snapshot = element.screenshot_as_png
		self.upload_snapshot(test_name=test_name, snapshot=snapshot)

		# self.driver.set_window_size(original_size['width'], original_size['height'])

	def add_custom_css(self, custom_css):
		self.original_style = self.driver.execute_script("return document.querySelector('style')")
		if self.original_style is not None:
			self.driver.execute_script(f"document.querySelector('style').innerHTML += '{custom_css}'")
		else:
			self.driver.execute_script(f"document.body.innerHTML += '<style>{custom_css}</style>'")

	def reset_css(self):
		if self.original_style is not None:
			self.driver.execute_script(f"document.querySelector('style').innerHTML = '{self.original_style}'")
		else:
			self.driver.execute_script(f"document.querySelector('style').innerHTML = ''")


	@keyword(name='Take Beholder Snapshot')
	def take_snapshot(self, custom_css: Optional[str] = None):
		"""
		Takes a snapshot of the current page and send to Beholder's platform to be build.

        ``custom_css`` argument specifies the custom css that will be added to the page for 
		the snapshot, this can be used to remove dynamic elements of the page. [optional]
		"""
		test_name = BuiltIn().get_variable_value("${TEST NAME}")
		print(test_name)
		self.capture_snapshot(test_name=test_name, custom_css=custom_css)


	@keyword(name='Take Beholder Element Snapshot')
	def take_snapshot(self, locator):
		"""
		Takes a snapshot from a element of the current page using the given locator and send to Beholder's platform to be build.

        ``locator`` argument specifies the element locator that will be uploaded.
		"""
		test_name = BuiltIn().get_variable_value("${TEST NAME}")
		print(test_name)
		self.capture_element_snapshot(locator=locator, test_name=test_name)
	