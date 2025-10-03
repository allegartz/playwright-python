"""
Setup configuration for Playwright Python Test Framework
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="playwright-test-framework",
    version="1.0.0",
    author="Playwright Test Team",
    description="Advanced Playwright Python Test Automation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "playwright>=1.40.0",
        "pytest>=7.4.3",
        "pytest-playwright>=0.4.4",
        "pytest-xdist>=3.5.0",
        "pytest-html>=4.1.1",
        "loguru>=0.7.2",
        "pydantic>=2.5.2",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "faker>=20.1.0",
        "jsonschema>=4.20.0",
        "tenacity>=8.2.3",
        "allure-pytest>=2.13.2",
    ],
)
