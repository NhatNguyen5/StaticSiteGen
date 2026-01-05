import unittest
import sys
from gen_content import extract_title
from logging_module.my_logging import logger


class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        skip_test = False
        if skip_test:
            return
        log = logger()
        log.enable = True
        log("==============================================")
        func_name = sys._getframe().f_code.co_name
        log(f"Test for: {func_name}")
        test_cases = [
"""
Hello
""",
"""
# Hello
""",
"""
#Hello
""",
"""
# Hello there
darkness

my old
friend
"""
        ]

        expected_results = [
            "Error",
            "Hello",
            "Error",
            "Hello there",
        ]

        run_test(self, extract_title, test_cases, expected_results, log)

def run_test(unit_test, test_function, test_cases, expected_results, log):
    log("==============================================")
    log(f"Test for: {sys._getframe(1).f_code.co_name}")
    case_number = 0
    for case, expected_result in zip(test_cases, expected_results):
        case_number += 1
        log(f"\nRunning case {case_number}")

        # unpack tuple
        def unpack():
            if isinstance(case, (tuple, list)):
                return test_function(*case)
            if isinstance(case, dict):
                return test_function(**case)
            return test_function(case)
        
        if expected_result == "Error":
            with unit_test.assertRaises(ValueError, msg=f"Case {case_number} failed") as e:
                unpack()
            log(f"Expected error: {e.exception}")
        else:
            result = unpack()
            unit_test.assertEqual(result, expected_result, msg=f"Case {case_number} failed")