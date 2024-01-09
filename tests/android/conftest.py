import allure
import allure_commons
import pytest
from appium import webdriver
from config import loaded_configuration, loaded_creds
from utils import attach

from appium.options.android import UiAutomator2Options
from selene import browser, support

from utils.resource_handler import path


@pytest.fixture(scope='function')
def configure_android_options():
    options = UiAutomator2Options()

    options.set_capability('deviceName', loaded_configuration.deviceName)
    options.set_capability('appWaitActivity', loaded_configuration.appWaitActivity)
    options.set_capability('app', (
        loaded_configuration.app if loaded_configuration.app.startswith('/') or loaded_configuration.app.startswith('bs://')
        else path(loaded_configuration.app)
    ))

    if loaded_configuration.context == 'remote':
        options.set_capability('platformVersion', loaded_configuration.platformVersion)
        options.set_capability(
            # Set other BrowserStack capabilities
            'bstack:options', {
                        "projectName": "First Python project",
                        "buildName": "browserstack-build-1",
                        "sessionName": "BStack first_test",

                        # Set your access credentials
                        "userName": loaded_creds.login,
                        "accessKey": loaded_creds.password,
            }
        )

    configure_browser(options)

    yield

    handle_attachments()


def handle_attachments():
    attach.attach_screenshot()
    attach.attach_screen_xml_dump()
    with allure.step('Tear down app session'):
        browser.quit()
    if loaded_configuration.context == 'remote':
        attach.attach_bstack_video(browser.driver.session_id)


def configure_browser(options):
    with allure.step('Init app session'):
        browser.config.driver = webdriver.Remote(
            loaded_configuration.server_url,
            options=options)

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext)
