"""
Factory Pattern

Factory classes for creating objects:
- Page Object Factory
- Test Data Factory
- Browser Factory
"""

from typing import Type, Dict, Any, Optional
from playwright.sync_api import Page
from loguru import logger
from faker import Faker

from ..core.page_base import BasePage


class PageFactory:
    """
    Factory for creating page objects
    
    Example:
        factory = PageFactory()
        factory.register("login", LoginPage)
        login_page = factory.create("login", page)
    """
    
    def __init__(self):
        """Initialize page factory"""
        self._pages: Dict[str, Type[BasePage]] = {}
        logger.debug("Page factory initialized")
    
    def register(self, name: str, page_class: Type[BasePage]):
        """
        Register a page class
        
        Args:
            name: Page identifier
            page_class: Page class
        """
        self._pages[name] = page_class
        logger.debug(f"Registered page: {name}")
    
    def create(self, name: str, page: Page) -> BasePage:
        """
        Create page instance
        
        Args:
            name: Page identifier
            page: Playwright Page instance
            
        Returns:
            Page object instance
        """
        if name not in self._pages:
            raise ValueError(f"Page not registered: {name}")
        
        page_class = self._pages[name]
        instance = page_class(page)
        logger.debug(f"Created page instance: {name}")
        return instance
    
    def get_registered_pages(self) -> list:
        """Get list of registered page names"""
        return list(self._pages.keys())


class TestDataFactory:
    """
    Factory for generating test data
    
    Example:
        factory = TestDataFactory()
        user_data = factory.create_user()
        email = factory.email()
    """
    
    def __init__(self, locale: str = "en_US"):
        """
        Initialize test data factory
        
        Args:
            locale: Faker locale
        """
        self.faker = Faker(locale)
        logger.debug(f"Test data factory initialized with locale: {locale}")
    
    def create_user(self, **overrides) -> Dict[str, Any]:
        """
        Create user test data
        
        Args:
            **overrides: Field overrides
            
        Returns:
            User data dictionary
        """
        user_data = {
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'email': self.faker.email(),
            'username': self.faker.user_name(),
            'password': self.faker.password(length=12),
            'phone': self.faker.phone_number(),
            'date_of_birth': self.faker.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        }
        user_data.update(overrides)
        return user_data
    
    def create_address(self, **overrides) -> Dict[str, Any]:
        """
        Create address test data
        
        Args:
            **overrides: Field overrides
            
        Returns:
            Address data dictionary
        """
        address_data = {
            'street': self.faker.street_address(),
            'city': self.faker.city(),
            'state': self.faker.state(),
            'zip_code': self.faker.zipcode(),
            'country': self.faker.country(),
        }
        address_data.update(overrides)
        return address_data
    
    def create_company(self, **overrides) -> Dict[str, Any]:
        """
        Create company test data
        
        Args:
            **overrides: Field overrides
            
        Returns:
            Company data dictionary
        """
        company_data = {
            'name': self.faker.company(),
            'email': self.faker.company_email(),
            'phone': self.faker.phone_number(),
            'website': self.faker.url(),
        }
        company_data.update(overrides)
        return company_data
    
    def email(self, domain: Optional[str] = None) -> str:
        """Generate email"""
        return self.faker.email(domain=domain)
    
    def name(self) -> str:
        """Generate full name"""
        return self.faker.name()
    
    def text(self, max_chars: int = 200) -> str:
        """Generate random text"""
        return self.faker.text(max_nb_chars=max_chars)
    
    def number(self, min_value: int = 0, max_value: int = 1000) -> int:
        """Generate random number"""
        return self.faker.random_int(min=min_value, max=max_value)
    
    def url(self) -> str:
        """Generate URL"""
        return self.faker.url()
    
    def uuid(self) -> str:
        """Generate UUID"""
        return self.faker.uuid4()
