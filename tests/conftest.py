from typing import Literal

import allure
import allure_commons
import pytest
from appium import webdriver

from utils import attach
from utils.resource_handler import path

import pydantic_settings
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selene import browser, support


class Configure(pydantic_settings.BaseSettings):
    login: str = 'dummy_value'
    password: str = 'dummy_value'
    android_url: str = 'dummy_value'
    ios_url: str = 'dummy_value'
    timeout: float = 20.0


config = Configure(_env_file=path(f'.env'))


@pytest.fixture(scope='function')
def configure_android_options():
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        "platformName": "android",
        "platformVersion": "13.0",
        "deviceName": "Samsung Galaxy S23 Ultra",

        # Set URL of the application under test
        "app": config.android_url,

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

    handle_attachments()

    # with allure.step('Close app'):
    #    browser.quit()


@pytest.fixture(scope='function')
def configure_ios_options():
    options = XCUITestOptions().load_capabilities({
        # Set URL of the application under test
        "app": config.ios_url,

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

    handle_attachments()
    # with allure.step('Close app'):
    #    browser.quit()


def handle_attachments():
    attach.attach_screenshot()
    attach.attach_screen_xml_dump()
    with allure.step('Tear down app session'):
        browser.quit()
    attach.attach_bstack_video(browser.driver.session_id)


def configure_browser(options):
    with allure.step('Init app session'):
        browser.config.driver = webdriver.Remote(
            'http://hub.browserstack.com/wd/hub',
            options=options)
    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options
    # browser.config.timeout = config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)
