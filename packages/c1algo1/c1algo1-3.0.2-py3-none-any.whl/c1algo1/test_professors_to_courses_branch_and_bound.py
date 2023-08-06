#!/usr/bin/env python3

import json
from professors_to_courses_branch_and_bound import generate_partial_schedule
with open('../data/input/sample_input.json') as f:
    input = json.load(f)

schedules = generate_partial_schedule(input, '2019')
#schedule = generate_partial_schedule(input)
#print(json.dumps(schedules[0], indent=2))
