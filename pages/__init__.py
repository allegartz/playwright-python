"""
Page objects package for Playwright tests.
"""
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.form_page import FormPage

__all__ = ["BasePage", "LoginPage", "FormPage"]
