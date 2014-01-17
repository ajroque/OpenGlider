#!/bin/python2
import sys
from optparse import OptionParser
try:
    import unittest2 as unittest
except NameError:
    import unittest

parser = OptionParser()
parser.add_option("-n", "--num", default=1, help="Number of loops")
parser.add_option("-a", "--run_all", default=False, help="Run all tests (including visual)")
parser.add_option("-p", "--pattern", help="Run a custom Pattern to find")
parser.add_option("-f", "--folder", default="tests")

args = parser.parse_args()[0]

if args.pattern:
    pattern = args.pattern
elif args.run_all:
    pattern = "*test*.py"
else:
    pattern = "test*.py"

loader = unittest.TestLoader().discover(args.folder, pattern)

for i in range(int(args.num)):
    print(">>>Running ("+str(i)+"/"+str(args.num)+")")
    test_results = unittest.TextTestRunner(verbosity=2).run(loader)
    print(">>>Errors: ", test_results.errors)
    print(">>>Failures: ", test_results.failures)