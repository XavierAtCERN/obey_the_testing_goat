from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

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
        time.sleep(1)

        self.check_for_row_in_list_table('1: First item of the list')

        # User is still invited to add another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Second item of the list')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)        

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: First item of the list')
        self.check_for_row_in_list_table('2: Second item of the list')

        # ...
        self.fail('Finish the test!')

        # More of the story
