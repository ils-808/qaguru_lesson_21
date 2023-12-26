import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


def test_search_appium_articles(configure_android_options):
    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).type('Appium')

    with allure.step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


def test_search_and_open_appium_articles(configure_android_options):
    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).type('Appium')
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')).click()

    # THEN
    with allure.step('Verify article title'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Appium'))
