import json
import csv
import datetime
from sqlite3 import complete_statement
from xml.dom import InuseAttributeErr
from .course import Course
from .time_slots import timeslots
from .validator import courses_1a, courses_1b, courses_2a, courses_2b, courses_3a, courses_3b, courses_4a, courses_4b

scheduled_courses = {'fall': [], 'spring': [], 'summer': []}
for i in range(54):
    scheduled_courses['fall'].append([])
    scheduled_courses['spring'].append([])
    scheduled_courses['summer'].append([])




def get_onstream_semester(course_name):
    onstream_value = ""
    for course_1a in courses_1a:
        if course_1a == course_name:
            onstream_value = "1A"
    for course_1b in courses_1b:
        if course_1b == course_name:
            onstream_value = "1B"
    for course_2a in courses_2a:
        if course_2a == course_name:
            onstream_value = "2A"
    for course_2b in courses_2b:
        if course_2b == course_name:
            onstream_value = "2B"
    for course_3a in courses_3a:
        if course_3a == course_name:
            onstream_value = "3A"
    for course_3b in courses_3b:
        if course_3b == course_name:
            onstream_value = "3B"
    for course_4a in courses_4a:
        if course_4a == course_name:
            onstream_value = "4A"
    for course_4b in courses_4b:
        if course_4b == course_name:
            onstream_value = "4B"
    return onstream_value



# Functions takes a list of integers as input. If all integers in the list are zero, a list of the same size containing all ones is returned. Otherwise, the original list is returned
def ensure_non_zeros(score_list):
    all_zeros = True
    for score in score_list:
        if score != 0:
            all_zeros = False
    if all_zeros:
        for score_index in range(len(score_list)):
            score_list[score_index] = 1
    return score_list


def generate_course_list(courses_and_profs):

    obj = get_ppw()
    courses_with_common_times = get_courses_with_common_times()

    complete_list = []

    fall_list = []
    spring_list = []
    summer_list = []

    # ELSE we schedule with branch and bound

    for current_semester in courses_and_profs['schedule']:
        for course in courses_and_profs['schedule'][current_semester]:
            # Make sure its not a pre-assigned course like chem 101
            if len(course['sections']) > 0:
                num_sections = len(course['sections'])
                num_assigned_profs = len(
                    [section['professor'] for section in course['sections'] if section['professor'] is not None])
                num_assigned_timeslots = len(
                    [section['timeSlots'] for section in course['sections'] if len(section['timeSlots']) > 0])
                if num_assigned_profs == num_sections and num_assigned_timeslots == num_sections:
                    # Every section has a prof assigned and a set of timeSlots so we don't want to include it in the scheduling
                    continue
            course_name = course['course']['code']
            if (course_name not in obj):
                continue
            sem = (obj[course_name]['OnstreamSemester'])
            season = current_semester

            prof = course['sections'][0]['professor']
            if (prof is not None):
                prof = prof['id']

            pref_timeslots = {}
            time_scores = []

            if course_name in courses_with_common_times[current_semester]:
                consecutive_offerings = courses_with_common_times[current_semester][course_name][1]
                if consecutive_offerings > 3:
                    
                    start_time = courses_with_common_times[current_semester][course_name][0][0].strip()
                    if start_time[0] == '0': start_time = start_time[1:]
                    end_time = courses_with_common_times[current_semester][course_name][0][1].strip()
                    if end_time[0] == '0': end_time = end_time[1:]
                    day_spread = courses_with_common_times[current_semester][course_name][0][2].strip()


                    TWF_index = 0 # indices 0 - 26
                    MTh_index = 0 # indices 27 - 53
                    assigned_to_slot = False

                    # Use first 27 indices for index into time slots
                    while( TWF_index < len(timeslots) ):
                        
                        if(timeslots[TWF_index]['start_time'] == start_time): # If start time, set assigned_slot to True
                            assigned_to_slot = True
                            if day_spread == "MTh" or day_spread == "MTF": # set MTh_index if scheduled on MTh
                                MTh_index = 27 + TWF_index

                        if assigned_to_slot: # If assigned slot, add course to list of scheduled courses
                            # make course object here
                            semester = get_onstream_semester(course_name)
                            scheduled_course = Course(course_name, semester, course['sections'][0]['professor']['id'], [], current_semester)

                            if day_spread == "MTh": # Check if course should be added at MTh index
                                scheduled_courses[current_semester][MTh_index].append(scheduled_course)
                            elif day_spread == "MTF": # If day spread is MTWF, add to both TWF and MTh indices
                                scheduled_courses[current_semester][MTh_index].append(scheduled_course)
                                scheduled_courses[current_semester][TWF_index].append(scheduled_course)
                            else: # Else add at TWF index
                                scheduled_courses[current_semester][TWF_index].append(scheduled_course)
                            
                            # If end time, set assigned_slots to False
                            if(timeslots[TWF_index]['end_time'] == end_time):
                                
                                assigned_to_slot = False

                                # Add scheduled courset to schedule json
                                if day_spread == "MTh": 
                                    scheduled_days = ["MONDAY", "THURSDAY"]
                                elif day_spread == "MTF":
                                    scheduled_days = ["MONDAY", "TUESDAY", "FRIDAY"]
                                else:
                                    scheduled_days = ["TUESDAY", "WEDNESDAY", "FRIDAY"]
                                    
                                for section in course['sections']:
                                    for scheduled_day in scheduled_days:
                                        section['timeSlots'].append({'dayOfWeek': scheduled_day, 'timeRange': (start_time, end_time)})
                                

                        # Increment indices
                        TWF_index += 1
                        MTh_index += 1
                    


            else:
                for instructor in courses_and_profs['professors']:
                    if prof is instructor['id']:

                        #    Generate List of PROF Preferences over 27 30minute

                        monday_thursday = [0] * 27
                        tuesday_wednesday_friday = [0] * 27

                        if (current_semester in instructor['preferredTimes']):

                            if instructor['preferredTimes'][current_semester] != None:
                                for day in instructor['preferredTimes'][current_semester]:
                                    curr_day_slots = [0] * 27

                                    for times in instructor['preferredTimes'][current_semester][day]:

                                        start_time = datetime.datetime.strptime(
                                            str(times[0]), "%H:%M")
                                        end_time = datetime.datetime.strptime(
                                            str(times[1]), "%H:%M")
                                        base_time = datetime.datetime(1900, 1, 1)

                                        # Converting Start Time / End Time into index

                                        min_to_start = (
                                            start_time - base_time).total_seconds() / 60
                                        min_to_end = (
                                            end_time - base_time).total_seconds() / 60

                                        # Subtract BASE Minutes (830 AM = 510minutes, divide by 30 to get starting index)
                                        starting_index = int(
                                            (min_to_start - 510) / 30)

                                        # Subtract BASE Minutes by 500 (As END TIME IS NOT a multiple of 30 (10 minutes less) and divide by 30 to get ending index)
                                        ending_index = int((min_to_end - 500) / 30)

                                        for i in range(starting_index, ending_index):

                                            curr_day_slots[i] = 1

                                            if day == 'monday' or day == 'thursday':
                                                monday_thursday[i] = monday_thursday[i] + 1

                                            if day == 'tuesday' or day == 'wednesday' or day == 'friday':
                                                tuesday_wednesday_friday[i] = tuesday_wednesday_friday[i] + 1

                                        pref_timeslots[day] = curr_day_slots

                        pref_timeslots['monday_thursday'] = monday_thursday
                        pref_timeslots['tuesday_wednesday_friday'] = tuesday_wednesday_friday
                        time_scores = tuesday_wednesday_friday + monday_thursday

                complete_list.append(
                    Course(course_name, sem, prof, time_scores, season))

                time_scores = ensure_non_zeros(time_scores)

                if current_semester == "fall":
                    fall_list.append(
                        Course(course_name, sem, prof, time_scores, season))
                elif current_semester == "spring":
                    spring_list.append(
                        Course(course_name, sem, prof, time_scores, season))
                if current_semester == "summer":
                    summer_list.append(
                        Course(course_name, sem, prof, time_scores, season))

    return [complete_list, fall_list, spring_list, summer_list]


def get_ppw():
    ppw = {
        "CSC111": {
            "CourseID": "CSC111",
            "CourseName": "Fundamentals of Programming with Engineering Applications",
            "OnstreamSemester": "1A",
            "OfferedIn": "F,Sp",
            "Capacity": 120
        },
        "ENGR110": {
            "CourseID": "ENGR110",
            "CourseName": "Design & Communication I",
            "OnstreamSemester": "1A",
            "OfferedIn": "F",
            "Capacity": 120
        },
        "ENGR130": {
            "CourseID": "ENGR130",
            "CourseName": "Introduction to Professional Practice",
            "OnstreamSemester": "1A",
            "OfferedIn": "F,Sp",
            "Capacity": 120
        },
        "MATH100": {
            "CourseID": "MATH100",
            "CourseName": "Calculus I",
            "OnstreamSemester": "1A",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },
        "MATH110": {
            "CourseID": "MATH110",
            "CourseName": "Matrix Algebra for Engineers",
            "OnstreamSemester": "1A",
            "OfferedIn": "F",
            "Capacity": 120
        },
        "PHYS110": {
            "CourseID": "PHYS110",
            "CourseName": "Introductory Physics I",
            "OnstreamSemester": "1A",
            "OfferedIn": "F,Sp",
            "Capacity": 120
        },

        "CSC115": {
            "CourseID": "CSC115",
            "CourseName": "Fundamentals of Prograaming: II",
            "OnstreamSemester": "1B",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "ENGR120": {
            "CourseID": "ENGR120",
            "CourseName": "Design & Communication II",
            "OnstreamSemester": "1B",
            "OfferedIn": "Sp",
            "Capacity": 120
        },

        "ENGR141": {
            "CourseID": "ENGR141",
            "CourseName": "Engineering Mechanics - Statics & Dynamics",
            "OnstreamSemester": "1B",
            "OfferedIn": "Sp,Su",
            "Capacity": 120
        },

        "MATH101": {
            "CourseID": "MATH101",
            "CourseName": "Integral Calculus with Applications",
            "OnstreamSemester": "1B",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "PHYS111": {
            "CourseID": "PHYS111",
            "CourseName": "Introductory Physics II",
            "OnstreamSemester": "1B",
            "OfferedIn": "Sp,Su",
            "Capacity": 120
        },

        "CSC230": {
            "CourseID": "CSC230",
            "CourseName": "Introduction to Computer Architecture",
            "OnstreamSemester": "2A",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "CHEM101": {
            "CourseID": "CHEM101",
            "CourseName": "Fundamentals of Chemistry from Atoms to Materials",
            "OnstreamSemester": "2A",
            "OfferedIn": "F,Su",
            "Capacity": 120
        },

        "ECE260": {
            "CourseID": "ECE260",
            "CourseName": "Continuous-Time Signals & Systems",
            "OnstreamSemester": "2A",
            "OfferedIn": "F,Su",
            "Capacity": 120
        },

        "MATH122": {
            "CourseID": "MATH122",
            "CourseName": "Logic & Foundations",
            "OnstreamSemester": "2A",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "SENG265": {
            "CourseID": "SENG265",
            "CourseName": "Software Development Methods",
            "OnstreamSemester": "2A",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "STAT260": {
            "CourseID": "STAT260",
            "CourseName": "Introduction to Probability & Statistics",
            "OnstreamSemester": "2A",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "CSC225": {
            "CourseID": "CSC225",
            "CourseName": "Algorithms & Data Structures I",
            "OnstreamSemester": "2B",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "ECE310": {
            "CourseID": "ECE310",
            "CourseName": "Digital Signal Processing I",
            "OnstreamSemester": "2B",
            "OfferedIn": "Sp,Su",
            "Capacity": 120
        },

        "ECON180": {
            "CourseID": "ECON180",
            "CourseName": "Introduction to Principles of Micro Economics",
            "OnstreamSemester": "2B",
            "OfferedIn": "F,Su",
            "Capacity": 120
        },

        "SENG275": {
            "CourseID": "SENG275",
            "CourseName": "Software Testing",
            "OnstreamSemester": "2B",
            "OfferedIn": "Sp,Su",
            "Capacity": 120
        },

        "SENG310": {
            "CourseID": "SENG310",
            "CourseName": "Human Computer Interaction",
            "OnstreamSemester": "2B",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "ECE458": {
            "CourseID": "ECE458",
            "CourseName": "Communication Networks",
            "OnstreamSemester": "3A",
            "OfferedIn": "Sp",
            "Capacity": 120
        },

        "CSC226": {
            "CourseID": "CSC226",
            "CourseName": "Algorithms & Data Structues II",
            "OnstreamSemester": "3A",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "ECE360": {
            "CourseID": "ECE360",
            "CourseName": "Control Theory & Systems",
            "OnstreamSemester": "3B",
            "OfferedIn": "F,Sp",
            "Capacity": 120
        },

        "SENG321": {
            "CourseID": "SENG321",
            "CourseName": "Requirements Engineering",
            "OnstreamSemester": "3A",
            "OfferedIn": "F,Sp",
            "Capacity": 120
        },

        "SENG371": {
            "CourseID": "SENG371",
            "CourseName": "Software Evolution",
            "OnstreamSemester": "3A",
            "OfferedIn": "Sp",
            "Capacity": 120
        },

        "ECE355": {
            "CourseID": "ECE355",
            "CourseName": "Microprocessor-Based Systems",
            "OnstreamSemester": "3B",
            "OfferedIn": "F",
            "Capacity": 120
        },

        "CSC320": {
            "CourseID": "CSC320",
            "CourseName": "Foundations of Computer Science",
            "OnstreamSemester": "3B",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "CSC360": {
            "CourseID": "CSC360",
            "CourseName": "Operating Systems",
            "OnstreamSemester": "3B",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "CSC370": {
            "CourseID": "CSC370",
            "CourseName": "Database Systems",
            "OnstreamSemester": "3B",
            "OfferedIn": "F,Sp,Su",
            "Capacity": 120
        },

        "SENG350": {
            "CourseID": "SENG350",
            "CourseName": "Software Architecture & Design",
            "OnstreamSemester": "3B",
            "OfferedIn": "F",
            "Capacity": 120
        },

        "SENG360": {
            "CourseID": "SENG360",
            "CourseName": "Security Engineering",
            "OnstreamSemester": "3B",
            "OfferedIn": "F",
            "Capacity": 120
        },

        "SENG426": {
            "CourseID": "SENG426",
            "CourseName": "Software Quality Engineering",
            "OnstreamSemester": "4A",
            "OfferedIn": "Su",
            "Capacity": 120
        },

        "SENG440": {
            "CourseID": "SENG440",
            "CourseName": "Embedded Systems",
            "OnstreamSemester": "4A",
            "OfferedIn": "Su",
            "Capacity": 120
        },

        "SENG499": {
            "CourseID": "SENG499",
            "CourseName": "Design Project II",
            "OnstreamSemester": "4A",
            "OfferedIn": "Su",
            "Capacity": 120
        },

        "ECE455": {
            "CourseID": "ECE455",
            "CourseName": "Real Time Computer System Design",
            "OnstreamSemester": "4B",
            "OfferedIn": "Sp",
            "Capacity": 120
        },

        "SENG401": {
            "CourseID": "SENG401",
            "CourseName": "Social & Professional Issues",
            "OnstreamSemester": "4B",
            "OfferedIn": "Sp",
            "Capacity": 120
        }

    }
    return ppw


def get_courses_with_common_times():
    courses_with_common_times = {
        "fall": {
            "CSC115": [
                [
                    "15:30",
                    "16:20",
                    "MTF"
                ],
                6
            ],
            "ECE360": [
                [
                    "09:30",
                    "10:20",
                    "MTF"
                ],
                4
            ],
            "SENG275": [
                [
                    "10:00",
                    "11:20",
                    "MTh"
                ],
                2
            ],
            "CSC575": [
                [
                    "10:00",
                    "11:20",
                    "MTh"
                ],
                2
            ],
            "CSC330": [
                [
                    "14:30",
                    "15:50",
                    "MTh"
                ],
                3
            ],
            "CSC101": [
                [
                    "18:00",
                    "20:50",
                    "W"
                ],
                2
            ]
        },
        "summer": {
            "CSC225": [
                [
                    "09:30",
                    "10:20",
                    "MTh"
                ],
                6
            ],
            "ECE260": [
                [
                    "10:30",
                    "11:20",
                    "TWF"
                ],
                4
            ],
            "ECE310": [
                [
                    "10:00",
                    "11:20",
                    "MTh"
                ],
                4
            ],
            "SENG265": [
                [
                    "12:30",
                    "13:20",
                    "TWF"
                ],
                6
            ],
            "SENG426": [
                [
                    "10:00",
                    "11:20",
                    "MTh"
                ],
                6
            ],
            "SENG440": [
                [
                    "08:30",
                    "09:50",
                    "MTh"
                ],
                6
            ],
            "SENG475": [
                [
                    "11:30",
                    "12:20",
                    "TWF"
                ],
                4
            ],
            "SENG299": [
                [
                    "12:30",
                    "13:20",
                    "TWF"
                ],
                2
            ]
        },
        "spring": {
            "CSC106": [
                [
                    "11:30",
                    "12:20",
                    "TWF"
                ],
                6
            ],
            "CSC110": [
                [
                    "10:00",
                    "11:20",
                    "MTh"
                ],
                6
            ],
            "CSC349A": [
                [
                    "08:30",
                    "09:50",
                    "MTh"
                ],
                6
            ],
            "CSC466": [
                [
                    "11:30",
                    "12:20",
                    "TWF"
                ],
                4
            ],
            "CSC503": [
                [
                    "09:30",
                    "10:20",
                    "TWF"
                ],
                2
            ],
            "CSC579": [
                [
                    "11:30",
                    "12:20",
                    "TWF"
                ],
                4
            ],
            "ECE310": [
                [
                    "10:30",
                    "11:20",
                    "TWF"
                ],
                3
            ],
            "ECE360": [
                [
                    "09:30",
                    "10:20",
                    "TWF"
                ],
                3
            ],
            "ECE458": [
                [
                    "13:00",
                    "14:20",
                    "MTh"
                ],
                3
            ],
            "SENG468": [
                [
                    "13:30",
                    "14:20",
                    "TWF"
                ],
                4
            ],
            "CSC101": [
                [
                    "18:00",
                    "20:50",
                    "W"
                ],
                2
            ],
            "SENG462": [
                [
                    "13:30",
                    "14:20",
                    "TWF"
                ],
                2
            ]
        }
    }

    return courses_with_common_times
