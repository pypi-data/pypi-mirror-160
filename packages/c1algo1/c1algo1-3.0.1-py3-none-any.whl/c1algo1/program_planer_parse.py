import json, csv

with open("../test/data/SENG_PPW.json", "r") as fh:
    obj = json.load(fh)

# create list of correlated courses by on stream semester offering

correlated_courses = {}
for item in obj:
    sem = obj[item]["OnstreamSemester"]
    if sem in correlated_courses:
        correlated_courses[sem] = correlated_courses[sem] + "," + item
    else:
        correlated_courses.update({sem : item})

# print(correlated_courses)
# print('-' * 75)

# create list of correlated courses by semester "Offered In"


schedule_by_semester={}
for item in obj:
    semesters = obj[item]["OfferedIn"]
    chunks = semesters.split(',')
    for sem in chunks:
        if sem in schedule_by_semester:
            schedule_by_semester[sem] = schedule_by_semester[sem] + "," + item
        else:
            schedule_by_semester.update({sem : item})
print(schedule_by_semester)
print('-' * 75)

# Access information regarding course in initial json file FROM created dictionaries

for item in schedule_by_semester:
    list_of_courses = schedule_by_semester[item]
    courses = list_of_courses.split(',')

    for course in courses:
        print(obj[course])

print('-' * 75)


