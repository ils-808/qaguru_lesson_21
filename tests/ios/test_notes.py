import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be


@pytest.mark.both
@pytest.mark.ios
def test_read_article(configure_ios_options):
    with allure.step('Select Web View tab'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Web View')).click()

    with allure.step('Verify the get demo is clickable'):
        browser.element((AppiumBy.ID, 'Get a demo')).should(be.clickable)
