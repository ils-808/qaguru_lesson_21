import pytest
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have



def test_getting_started(configure_android_options):
    with allure.step('Verify first welcome screen'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/primaryTextView')).should(have.text('The Free Encyclopedia\n…in over 300 languages'))

    with allure.step('Press Continue button'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_forward_button')).click()
    with allure.step('Verify second welcome screen'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/primaryTextView')).should(have.text('New ways to explore'))

    with allure.step('Press Continue button'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_forward_button')).click()
    with allure.step('Verify third welcome screen'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/primaryTextView')).should(have.text('Reading lists with sync'))

    with allure.step('Press Continue button'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_forward_button')).click()
    with allure.step('Verify fourth welcome screen'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/primaryTextView')).should(have.text('Send anonymous data'))

def test_search_appium_articles(configure_android_options):
    with allure.step('Skip intro'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")).click()
    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')

    with allure.step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


def test_search_and_open_appium_articles(configure_android_options):
    with allure.step('Skip intro'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_skip_button")).click()
    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')).click()

    # THEN
    with allure.step('Verify article title'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Appium'))
