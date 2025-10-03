#!/usr/bin/env python3
"""
Test runner script for Playwright tests.
Provides convenient commands to run different test suites.
"""
import sys
import subprocess


def run_all_tests():
    """Run all tests."""
    print("Running all tests...")
    subprocess.run([
        "pytest",
        "tests/",
        "-v",
        "--html=reports/report.html",
        "--self-contained-html"
    ])


def run_login_tests():
    """Run only login tests."""
    print("Running login tests...")
    subprocess.run([
        "pytest",
        "tests/",
        "-m", "login",
        "-v",
        "--html=reports/login_report.html",
        "--self-contained-html"
    ])


def run_form_tests():
    """Run only form tests."""
    print("Running form tests...")
    subprocess.run([
        "pytest",
        "tests/",
        "-m", "form",
        "-v",
        "--html=reports/form_report.html",
        "--self-contained-html"
    ])


def run_ui_tests():
    """Run only UI tests."""
    print("Running UI tests...")
    subprocess.run([
        "pytest",
        "tests/",
        "-m", "ui",
        "-v",
        "--html=reports/ui_report.html",
        "--self-contained-html"
    ])


def run_flow_tests():
    """Run only flow tests."""
    print("Running user flow tests...")
    subprocess.run([
        "pytest",
        "tests/",
        "-m", "flow",
        "-v",
        "--html=reports/flow_report.html",
        "--self-contained-html"
    ])


def run_smoke_tests():
    """Run only smoke tests."""
    print("Running smoke tests...")
    subprocess.run([
        "pytest",
        "tests/",
        "-m", "smoke",
        "-v",
        "--html=reports/smoke_report.html",
        "--self-contained-html"
    ])


def run_regression_tests():
    """Run only regression tests."""
    print("Running regression tests...")
    subprocess.run([
        "pytest",
        "tests/",
        "-m", "regression",
        "-v",
        "--html=reports/regression_report.html",
        "--self-contained-html"
    ])


def run_headed():
    """Run tests in headed mode (visible browser)."""
    print("Running tests in headed mode...")
    subprocess.run([
        "pytest",
        "tests/",
        "-v",
        "--headed",
        "--html=reports/report.html",
        "--self-contained-html"
    ])


def run_specific_test(test_path):
    """Run a specific test file or test function."""
    print(f"Running specific test: {test_path}")
    subprocess.run([
        "pytest",
        test_path,
        "-v",
        "--html=reports/specific_report.html",
        "--self-contained-html"
    ])


def show_help():
    """Display help information."""
    help_text = """
Playwright Test Runner
======================

Usage: python run_tests.py [command] [options]

Commands:
    all             Run all tests
    login           Run login tests only
    form            Run form tests only
    ui              Run UI tests only
    flow            Run user flow tests only
    smoke           Run smoke tests only
    regression      Run regression tests only
    headed          Run tests with visible browser
    test <path>     Run specific test file or function
    help            Show this help message

Examples:
    python run_tests.py all
    python run_tests.py login
    python run_tests.py smoke
    python run_tests.py test tests/test_login.py
    python run_tests.py test tests/test_login.py::TestLogin::test_successful_login

Reports will be generated in the reports/ directory.
"""
    print(help_text)


def main():
    """Main entry point for the test runner."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    # Create reports directory if it doesn't exist
    import os
    os.makedirs("reports", exist_ok=True)
    
    if command == "all":
        run_all_tests()
    elif command == "login":
        run_login_tests()
    elif command == "form":
        run_form_tests()
    elif command == "ui":
        run_ui_tests()
    elif command == "flow":
        run_flow_tests()
    elif command == "smoke":
        run_smoke_tests()
    elif command == "regression":
        run_regression_tests()
    elif command == "headed":
        run_headed()
    elif command == "test":
        if len(sys.argv) < 3:
            print("Error: Please specify a test path")
            print("Usage: python run_tests.py test <test_path>")
            return
        run_specific_test(sys.argv[2])
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()
