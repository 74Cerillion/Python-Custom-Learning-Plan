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