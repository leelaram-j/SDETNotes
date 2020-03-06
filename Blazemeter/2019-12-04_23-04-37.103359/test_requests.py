# coding=utf-8

import logging
import random
import string
import sys
import unittest
from time import time, sleep

import apiritif

import os
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as econd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

def setup():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service_log_path='/Users/lee/Documents/SDET_Master/Blazemeter/2019-12-04_23-04-37.103359/webdriver.log', chrome_options=options)
    driver.implicitly_wait(60.0)
    wnd_mng = WindowManager(driver)
    frm_mng = FrameManager(driver)
    vars = {
        
    }
    apiritif.put_into_thread_store(vars, driver, wnd_mng, frm_mng)


def teardown():
    (_, driver, _, _) = apiritif.get_from_thread_store()
    driver.quit()

class TestDemotestSelenium(unittest.TestCase):

    def setUp(self):
        (self.vars, self.driver, self.wnd_mng, self.frm_mng) = apiritif.get_from_thread_store()

    def test_1_Test(self):
        try:
            self.driver.execute_script('/* FLOW_MARKER test-case-start */', {
                'testCaseName': 'Test',
                'testSuiteName': 'DemoTest-Selenium',
            })
            with apiritif.transaction_logged('Test'):
                self.driver.get('chrome://newtab/')
                self.driver.get('https://www.google.com/')
                self.driver.find_element(By.NAME, 'q').click()
                self.driver.find_element(By.NAME, 'q').clear()
                self.driver.find_element(By.NAME, 'q').send_keys('Selenium Test')
                self.driver.find_element(By.NAME, 'q').send_keys(Keys.ENTER)
        except AssertionError as exc:
            self.driver.execute_script('/* FLOW_MARKER test-case-stop */', {
                'status': 'failed',
                'message': str(exc),
            })
            raise
        except BaseException as exc:
            self.driver.execute_script('/* FLOW_MARKER test-case-stop */', {
                'status': 'broken',
                'message': str(exc),
            })
            raise
        else:
            self.driver.execute_script('/* FLOW_MARKER test-case-stop */', {
                'status': 'success',
                'message': '',
            })
from selenium.common.exceptions import NoSuchWindowException, NoSuchFrameException

class FrameManager():

    def __init__(self, driver):
        self.driver = driver

    def switch(self, frame_name=None):
        try:
            if ((not frame_name) or (frame_name == 'relative=top')):
                self.driver.switch_to_default_content()
            elif frame_name.startswith('index='):
                self.driver.switch_to.frame(int(frame_name.split('=')[1]))
            elif (frame_name == 'relative=parent'):
                self.driver.switch_to.parent_frame()
            else:
                self.driver.switch_to.frame(frame_name)
        except NoSuchFrameException:
            raise NoSuchFrameException(('Invalid Frame ID: %s' % frame_name))

class WindowManager():

    def __init__(self, driver):
        self.driver = driver
        self.windows = {
            
        }

    def switch(self, window_name=None):
        try:
            if (not window_name):
                self.driver.switch_to.window(self.driver.window_handles[(- 1)])
            elif window_name.isdigit():
                self._switch_by_idx(int(window_name))
            elif window_name.startswith('win_ser_'):
                self._switch_by_win_ser(window_name)
            else:
                self.driver.switch_to.window(window_name)
        except NoSuchWindowException:
            raise NoSuchWindowException(('Invalid Window ID: %s' % window_name))

    def _switch_by_idx(self, win_index):
        wnd_handlers = self.driver.window_handles
        if ((len(wnd_handlers) <= win_index) and (win_index >= 0)):
            self.driver.switch_to.window(wnd_handlers[win_index])
        else:
            raise NoSuchWindowException(('Invalid Window ID: %s' % str(win_index)))

    def _switch_by_win_ser(self, window_name):
        if (window_name == 'win_ser_local'):
            wnd_handlers = self.driver.window_handles
            if (len(wnd_handlers) > 0):
                self.driver.switch_to.window(wnd_handlers[0])
            else:
                raise NoSuchWindowException(('Invalid Window ID: %s' % window_name))
        else:
            if (window_name not in self.windows):
                self.windows[window_name] = self.driver.window_handles[(- 1)]
            self.driver.switch_to.window(self.windows[window_name])

    def close(self, window_name=None):
        if window_name:
            self.switch(window_name)
        self.driver.close()
