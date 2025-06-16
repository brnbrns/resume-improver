#!/usr/bin/env python3
"""
Simple test runner for the resume improver project.
Runs all tests and provides basic reporting.
"""

import unittest
import sys
import os
from io import StringIO

def run_tests():
    """Run all tests and provide basic reporting."""
    # Capture test output
    test_output = StringIO()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Count tests
    test_count = suite.countTestCases()
    
    print(f"Discovered {test_count} tests")
    print("="*50)
    
    runner = unittest.TextTestRunner(
        stream=test_output, 
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    result = runner.run(suite)
    
    # Print results
    output = test_output.getvalue()
    print(output)
    
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    
    # Return success/failure based on test results
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Resume Improver Test Suite")
    print("="*50)
    success = run_tests()
    sys.exit(0 if success else 1)
