#!/usr/bin/env python3

import json
import sys
import os

from tools import *

# with open('../test/data/sample_input.json') as f:
#     scheduler_input = json.load(f)

# associated = associate_profs_with_courses(scheduler_input=scheduler_input)
# print(json.dumps(associated, indent=2))

with open('../test/data/test_sort.json') as f:
    input_with_interested_profs = json.load(f)

sorted = sort_courses_by_prof_interest(input_with_interested_profs=input_with_interested_profs)
print(json.dumps(sorted, indent=2))
