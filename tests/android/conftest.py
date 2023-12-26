# from typing import Literal
#
# import pytest
#
# from utils import attach
# from utils.resource_handler import path
#
# import pydantic_settings
# from appium.options.android import UiAutomator2Options
# from appium.options.ios import XCUITestOptions
# from selene import browser
#
#
# class Configure(pydantic_settings.BaseSettings):
#     context: Literal['ios', 'android'] = 'android'
#     login: str = 'dummy_value'
#     password: str = 'dummy_value'
#     ios_url: str = 'dummy_value'
#     android_url: str = 'dummy_value'
#     timeout: float = 10.0
#
#
# config = Configure(_env_file=path(f'.env.{Configure().context}'))
#
#
# @pytest.fixture(scope='function', autouse=True)
# def configure_browserstack():
#     if config.context == 'android':
#         options = UiAutomator2Options().load_capabilities({
#             # Specify device and os_version for testing
#             "platformName": "android",
#             "platformVersion": "9.0",
#             "deviceName": "Google Pixel 3",
#
#             # Set URL of the application under test
#             "app": config.android_url,
#
#             # Set other BrowserStack capabilities
#             'bstack:options': {
#                 "projectName": "First Python project",
#                 "buildName": "browserstack-build-1",
#                 "sessionName": "BStack first_test",
#
#                 # Set your access credentials
#                 "userName": config.login,
#                 "accessKey": config.password,
#             }
#         })
#     else:
#         options = XCUITestOptions().load_capabilities({
#             # Set URL of the application under test
#             "app": config.ios_url,
#
#             # Specify device and os_version for testing
#             "deviceName": "iPhone 11 Pro",
#             "platformName": "ios",
#             "platformVersion": "13",
#
#             # Set other BrowserStack capabilities
#             "bstack:options": {
#                 "userName": config.login,
#                 "accessKey": config.password,
#                 "projectName": "First Python project",
#                 "buildName": "browserstack-build-1",
#                 "sessionName": "BStack first_test"
#             }
#         })
#
#     browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
#     browser.config.driver_options = options
#
#     browser.config.timeout = config.timeout
#
#     yield
#
#     attach.add_screenshot(browser)
#     attach.add_html(browser)
#     attach.add_logs(browser)
#     attach.add_video(browser)
#
#     browser.quit()

import pytest
from appium.options.android import UiAutomator2Options
from selene import browser
import os

from selenium import webdriver


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        # "platformName": "android",
        "platformVersion": "9.0",
        "deviceName": "Google Pixel 3",

        # Set URL of the application under test
        "app": "bs://sample.app",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "First Python project",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack first_test",

            # Set your access credentials
            "userName": "iakivkramarenko_qKHOLN",
            "accessKey": "FSHAmndKHW3XsDkgm5zT"
        }
    })

    # browser.config.driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)
    browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    browser.config.driver_options = options

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    browser.quit()
