
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import requests
import os

class DejavuLibrary(object):

	def __init__(self):
		self.original_style = None
		self.dejavu_url = 'http://127.0.0.1:8000'
		self.build_number = None

	def get_driver(self):
		selib = BuiltIn().get_library_instance('SeleniumLibrary')
		return selib.driver

	def start_build(self):
		self.build_number = BuiltIn().get_variable_value("${DEJAVU_BUILD_NUMBER}")
		if self.build_number is None:
			payload = {
				'token': os.environ['DEJAVU_TOKEN'],
				'build_number': 'None'
			}
			response = requests.post(f"{self.dejavu_url}/api/v1/start_app_build", data=payload)
			self.build_number = response.json()['build_number']
			BuiltIn().set_global_variable('${DEJAVU_BUILD_NUMBER}', self.build_number)

	def upload_snapshot(self, test_name, snapshot):
		
		payload = payload = {
				'token': os.environ['DEJAVU_TOKEN'],
				'build_number': self.build_number,
				'test_name': test_name
			}

		files = {
			'snapshot_image': ('snapshot_image.png', snapshot,'image/png'),
			}

		response = requests.post(f"{self.dejavu_url}/api/v1/upload_snapshot", data=payload, files=files)

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


	@keyword(name='Take Dejavu Snapshot')
	def take_snapshot(self, custom_css=None):
		test_name = BuiltIn().get_variable_value("${TEST NAME}")
		self.capture_snapshot(test_name=test_name, custom_css=custom_css)
