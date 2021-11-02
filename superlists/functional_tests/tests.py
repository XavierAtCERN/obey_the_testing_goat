from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes to check the homepage
        self.browser.get(self.live_server_url)

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User types "New item to the list" into a text box)
        inputbox.send_keys('First item of the list')

        # User hits enter, the page updates, and not the page lists item
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: First item of the list')

        # User is still invited to add another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Second item of the list')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: First item of the list')
        self.wait_for_row_in_list_table('2: Second item of the list')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('First item of the list')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: First item of the list')

        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')

        # New user comes along
        
        ## We use a new browser session to make sure that no information
        ## is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('First item of the list', page_text)
        self.assertNotIn('Whatever', page_text)

        # New user starts a list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('First item of new list')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: First item of new list')

        # New user gets his own unique URL
        newuser_list_url = self.browser.current_url
        self.assertRegex(newuser_list_url, '/lists/.+')
        self.assertNotEqual(newuser_list_url, user_list_url)

        # Still no trace of previous user list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('First item of the list', page_text)
        self.assertIn('First item of new list', page_text)

        # ...
        self.fail('Finish the test!')

