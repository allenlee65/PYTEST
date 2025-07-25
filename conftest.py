import pytest
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import TestResultCollector
from uiTests.automation_exercise_test import TestResultCollector

def pytest_runtest_logreport(report):
    """Pytest hook to capture test results"""
    if report.when == 'call':
        test_name = report.nodeid.split('::')[-1]
        
        if report.passed:
            TestResultCollector.add_result(test_name, 'PASSED')
        elif report.failed:
            error_msg = str(report.longrepr) if report.longrepr else 'Unknown error'
            TestResultCollector.add_result(test_name, 'FAILED', error_msg)
        elif report.skipped:
            TestResultCollector.add_result(test_name, 'SKIPPED')

def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    TestResultCollector.reset_results()

def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished"""
    TestResultCollector.send_test_report_email()