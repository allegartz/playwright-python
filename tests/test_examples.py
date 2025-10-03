"""
Example test demonstrating basic Playwright usage.
This test can be run against any website to verify the framework is working.
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_playwright_example_google(page: Page):
    """
    Example test navigating to Google and verifying the title.
    This demonstrates that Playwright is working correctly.
    """
    # Navigate to Google
    page.goto("https://www.google.com")
    
    # Verify the page title contains "Google"
    expect(page).to_have_title(lambda title: "Google" in title)
    
    # Verify the search box is visible
    search_box = page.get_by_role("combobox", name="Search")
    expect(search_box).to_be_visible()


@pytest.mark.smoke
def test_playwright_example_github(page: Page):
    """
    Example test navigating to GitHub and checking elements.
    """
    # Navigate to GitHub
    page.goto("https://github.com")
    
    # Wait for the page to load
    page.wait_for_load_state("networkidle")
    
    # Verify the URL
    assert "github.com" in page.url
    
    # Take a screenshot
    page.screenshot(path="tests/test_data/github_screenshot.png")


@pytest.mark.smoke  
def test_playwright_example_wikipedia(page: Page):
    """
    Example test demonstrating search functionality on Wikipedia.
    """
    # Navigate to Wikipedia
    page.goto("https://en.wikipedia.org")
    
    # Find the search input
    search_input = page.get_by_role("searchbox")
    
    # Type "Playwright"
    search_input.fill("Playwright")
    
    # Press Enter
    search_input.press("Enter")
    
    # Wait for navigation
    page.wait_for_load_state("networkidle")
    
    # Verify we're on a results or article page
    assert "wikipedia.org" in page.url


def test_playwright_viewport_example(page: Page):
    """
    Example test demonstrating viewport manipulation.
    """
    # Test mobile viewport
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto("https://www.google.com")
    page.wait_for_load_state("networkidle")
    
    # Test tablet viewport
    page.set_viewport_size({"width": 768, "height": 1024})
    page.wait_for_load_state("networkidle")
    
    # Test desktop viewport
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.wait_for_load_state("networkidle")
    
    assert True


def test_playwright_navigation_example(page: Page):
    """
    Example test demonstrating navigation.
    """
    # Navigate to first page
    page.goto("https://playwright.dev")
    page.wait_for_load_state("networkidle")
    first_url = page.url
    
    # Navigate to second page
    page.goto("https://playwright.dev/python/")
    page.wait_for_load_state("networkidle")
    
    # Go back
    page.go_back()
    page.wait_for_load_state("networkidle")
    
    # Verify we're back at the first URL
    assert page.url == first_url or page.url.rstrip('/') == first_url.rstrip('/')
    
    # Go forward
    page.go_forward()
    page.wait_for_load_state("networkidle")
    
    # Verify we're at Python docs
    assert "python" in page.url.lower()


@pytest.mark.ui
def test_playwright_element_interaction_example(page: Page):
    """
    Example test demonstrating element interactions.
    """
    page.goto("https://www.google.com")
    
    # Find search box
    search_box = page.get_by_role("combobox", name="Search")
    
    # Verify it's visible
    expect(search_box).to_be_visible()
    
    # Verify it's editable
    expect(search_box).to_be_editable()
    
    # Type text
    search_box.fill("Playwright Python")
    
    # Verify the text was entered
    expect(search_box).to_have_value("Playwright Python")
