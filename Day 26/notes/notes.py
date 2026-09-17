"""What is unit testing and what does it actually test?

The process of testing the smallest functional unit of code.
Helps ensure code quality and function. Write the unit test,
then run it every time you modify that code to ensrue it
still works. 

What is a unit test?

A block of code that verifies the accuracy of smaller,
isolated blocks of code, typically a function or method

Test Types:
Logic Checks:
    Does the system perform the right calculations and follow the
    right path through the code given a correct, expected input?
Boundary Checks:
    For the given inputs, how does the system respond? Edge Cases?
    Invalid Inputs?
Error Handling:
    When there are errors in inputs, how does the system respond?
Object-Oriented Checks:
    If the state of any persistent objects is changed by running
    the code, is the object updated correctly?
"""

"""Test Suite vs Test Case

Test Suite: A bunch of test cases grouped for a specific purpose.
    Tests multiple scenarios and functionalities

Test Case: A part of a test suite. Focuses on one particular
    aspect or scenario.
    Tests one scenario or functionality
"""

"""Arrange -> Act -> Assert

The Non-Security based AAA. A pattern for writing good tests:
Arrange: Inputs and Targets. Steps should set up the test case
    Does the test require any objects or special settings? Does
    it need a prep to database? Does it need to log into a web
    app? Handle all of these operations at the start of the test
Act: On the target behavior. Steps should cover the main thing 
    to be tested. This could be calling a function or method, a
    REST API, or interacting on a web page. Keep actions focused
    on the target behavior.
Assert: Expected Outcomes. Steps verify the goodness or badness
    of the output/response from the 'act' steps.

SEE EXAMPLE BELOW
The Arrange step creates a variable named “negative” for testing.
The Act step calls the “abs” function using the “negative” variable 
    and stores the returned value in a variable named “answer.”
The Assert step verifies that “answer” is a positive value.
"""
def test_abs_for_a_negative_number():
 
  # Arrange
  negative = -5
   
  # Act
  answer = abs(negative)
   
  # Assert
  assert answer == 5

"""Assertions
The fundamental tool used to verify that your code behaves as
    expected

If a condition matches your expectation, the test continues
else it fails and an exception is raised and the test runner flags
    it as a failure
"""

"""Happy-Path Testing
Happy Path testing is a technique that tests the application through a
    positive flow to generate a default output. 
Focuses on the most common and expected scenarios that a user will
    encounter when using an application. Assumes that the user wil
    follow the intended steps and provide valid inputs, and that the
    application will behave as expected.
Purpose: Verifies that the application can handle the normal and
    expected use cases without any errors or bugs. 
    Ensures app meets requirements like performance, usability, security
    and reliability
"""

"""Boundary/Edge Case Testing
Software testing/QA practice used to evaluate how a system behaves at
    its limits, operational thresholds, or under rare, unexpected
    conditions

Boundary Testing:
    Often called BVA (or Boundary Value Testing)
    Focuses heavily on the exact limits of the specific input range
    It tests the minimum, maximum, just inside, and just outside the
        accepted boundaries
    
Edge Case Testing:
    Involves evaluating scenarios that happen outside of standard
        operating procedures, typically involving unique user behaviors,
        complex interactions, or extreme stress. The opposite of the
        'Happy Path'
"""

"""Failure Testing
AKA Negative Testing or Error Path Testing

A software testing methodology designed to see how a software handles
    unexpected inputs, invalid data, or system exceptions

Core objective is ensuring that the system can fail gracefully.
"""

"""Test Isolation
Practice used to gather evidence about a defined risk, behavior, boundary,
    or operation condition.
Used to pick good tests that produce useful evidence instead of ceremonial
    checks that only create activity. 
Starts with a risk rather than a tool. If a service must remain responsive
    during a traffic surge, start by designing the load shape, response
    threshold, and observation window. From there, design tests that give
    information on those things, rather than just testing anything and
    everything and hoping the data is cohesive enough to get picture of
    responsiveness during a traffic surge
"""

"""Deterministic Tests
Software tests that always produce the exact same pass or fail result when
    run with the same starting state and inputs.
The contain no randomness, no hidden time dependencies, no external work
    calls that change outcomes between runs. 
"""

"""Fixtures
A fixed, known state or set of inputs used as a baseline to run software
    tests reliably and repeatedly. AKA your Test Data.
"""

"""Dependency Isolation
The practice of ensuring an application uses only its explicitly declared
    third-party libraries and runtime tools, preventing hidden system packages
    or other projects from interfering
"""

"""External Services in UnitTests
Poor dependencies because they introduce slow performance, flakiness, and lack
    of control into the testing process. They bring another potential layer of
    failure, which reduces the tests effectiveness. 
They're non-deterministic and lack isolation because of external factors outside
    the control of code or codebase itself.
"""

#Testing can't tell you what's wrong with your code, only what's not wrong with it

#HOW TO UNIT TEST IN PYTHON
"""
unittest is built into the PSL
A test case is created by inheriting from unittest
"""
def add(a, b):
   return a+b
import unittest
class AddTest(unittest.TestCase):
    def test_addition(self):
       self.assertEqual(add(2, 3), 5)

#output will be:
#---------------------------------------------
# Ran test in 0.0000s
# OK

#what's actually happening up there?
#add is the function we're testing
# we import unittest to write the test
# define a class that inherits from PSL's unittest
# define a test to run:
#   this specific test is a deterministic, happy-path test case that
#   isolates addition. The fixtures are 2 and 3. The assertion is 5.

"""Different assert methods in unittest
.assertEquals(a, b) = check is a == b
.assertTrue(x) = Check is bool(x) == True
.assertIsInstance(a, b) = check if a is an instance of class b
.assertIsNone(x) = ensures x is None
.assertFalse(x) = reverse of .assertTrue
.assertIs(a, b) = check is a is identical to b
.assertIn(a, b) = check is a is a member of b
"""

import unittest

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        pass

    # Returns True if the string contains 4 a.
    def test_strings_a(self):
        self.assertEqual('a'*4, 'aaaa')

    # Returns True if the string is in upper case.
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_strip(self):
        s = 'geeksforgeeks'
        self.assertEqual(s.strip('geek'), 'sforgeeks')

    # Returns true if the string splits and matches
    # the given output.
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()