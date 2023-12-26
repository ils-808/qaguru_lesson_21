from typing import Literal

import allure
import allure_commons
import pytest
from selenium import webdriver

from utils import attach
from utils.resource_handler import path

import pydantic_settings
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selene import browser, support


class Configure(pydantic_settings.BaseSettings):
    context: Literal['ios', 'android'] = 'android'
    login: str = 'dummy_value'
    password: str = 'dummy_value'
    url: str = 'dummy_value'
    timeout: float = 20.0


print(path(f'.env.{Configure().context}'))
config = Configure(_env_file=path(f'.env.{Configure().context}'))


@pytest.fixture(scope='function')
def configure_android_options():
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        "platformName": "android",
        "platformVersion": "9.0",
        "deviceName": "Google Pixel 3",

        # Set URL of the application under test
        "app": config.url,

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "First Python project",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack first_test",

            # Set your access credentials
            "userName": config.login,
            "accessKey": config.password,
        }
    })

    configure_browser(options)

    yield

    # handle_attachments()

    with allure.step('Close app'):
        browser.quit()


@pytest.fixture(scope='function')
def configure_ios_oprtions():
    options = XCUITestOptions().load_capabilities({
        # Set URL of the application under test
        "app": config.url,

        # Specify device and os_version for testing
        "deviceName": "iPhone 11 Pro",
        "platformName": "ios",
        "platformVersion": "13",

        # Set other BrowserStack capabilities
        "bstack:options": {
            "userName": config.login,
            "accessKey": config.password,
            "projectName": "First Python project",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack first_test"
        }
    })

    configure_browser(options)

    yield

    # handle_attachments()
    with allure.step('Close app'):
        browser.quit()


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
#             "app": config.url,
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
#             "app": config.url,
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
#     configure_browser(options)
#
#     yield
#
#     handle_attachments()
#
#     browser.quit()


def handle_attachments():
    attach.attach_screenshot()
    attach.attach_bstack_video(browser.driver.session_id)
    attach.attach_screen_xml_dump()


def configure_browser(options):
    browser.config.driver = webdriver.Remote('http://hub.browserstack.com/wd/hub', options=options)
    # browser.config.driver = webdriver.
    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options
    # browser.config.timeout = config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)
