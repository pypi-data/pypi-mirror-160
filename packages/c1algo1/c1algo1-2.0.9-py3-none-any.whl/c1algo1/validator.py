from datetime import datetime, timedelta
import traceback
import json, pickle
import copy

# check to see if every course has at least one section
def check_all_courses_have_section(schedule):
    error = []
    for semester in schedule:
        for course in schedule[semester]:
            if len(course['sections']) == 0:
                error.append(f"{course['course']['code']}/{semester} has no sections.")

    return error

# check to see if all sections have timeslots
def check_all_sections_have_timeslots(schedule):
    error = []
    for semester in schedule:
        for course in schedule[semester]:
            for section in course['sections']:
                if len(section['timeSlots']) == 0:
                    error.append(f"{course['course']['code']}/{semester} has sections with no timeslots.")

    return error

# check to see if all sections have professors
def check_all_sections_have_professor(schedule):
    error = []
    for semester in schedule:
        for course in schedule[semester]:
            for section in course['sections']:
                if not section['professor']:
                    error.append(f"{course['course']['code']}/{semester} has sections with no professor.")

    return error

# check to see if correlated courses for a given term do not overlap timeslots at any point
def check_no_correlated_courses_overlap(schedule):
    error = []

    # Compares a section 'other' with section 'question', returns false if the sections have time overlap
    def compare_sections(other_course_section, course_in_question_section):
        # For each pair of timeslots check for overlap
        for other_course_timeslot in other_course_section['timeSlots']:
            for course_in_question_timeslot in course_in_question_section['timeSlots']:
                # Make sure they're on the same day
                if other_course_timeslot['dayOfWeek'] == course_in_question_timeslot['dayOfWeek']:
                    other_start = datetime.strptime(other_course_timeslot['timeRange'][0], '%H:%M')
                    other_end = datetime.strptime(other_course_timeslot['timeRange'][1], '%H:%M')
                    question_start = datetime.strptime(course_in_question_timeslot['timeRange'][0], '%H:%M')
                    question_end = datetime.strptime(course_in_question_timeslot['timeRange'][1], '%H:%M')

                    #       |---------| other
                    # |---------| question
                    if other_start < question_end and other_end > question_end:
                        return False

                    # |----------| other
                    # |----------| question
                    if other_start == question_start and other_end == question_end:
                        return False

                    # |----------| other
                    #       |----------| question
                    if question_start < other_end and question_end > other_end:
                        return False
        return True

    def correlation_check(course_in_question, semester, stream):
        # Remove the course from stream so we don't do the symmetrical checks
        stream.remove(course_in_question['course']['code'])

        # Check the courses timeslots against every other stream course                
        # Then for each other course in stream make sure none of its timeslots are in this courses timeslots
        for other_code in stream:
            # Find the other course in the schedule
            for other_course in schedule[semester]:
                if other_code == other_course['course']['code']:
                    non_overlapping_sections_found = False
                    # For each pair of sections compare their timeslots
                    for other_course_section in other_course['sections']:
                        for course_in_question_section in course_in_question['sections']:
                            if compare_sections(other_course_section, course_in_question_section):
                                non_overlapping_sections_found = True
                    if not non_overlapping_sections_found:
                        error.append(f"{course_in_question['course']['code']} is correlated with {other_course['course']['code']} but all their sections overlap in {semester}.")                                         
    
    for semester in schedule:
        for course_in_question in schedule[semester]:
            course_in_question_code = course_in_question['course']['code']
            if course_in_question_code in courses_1a:
                correlation_check(course_in_question, semester, courses_1a)
            elif course_in_question_code in courses_1b:
                correlation_check(course_in_question, semester, courses_1b)
            elif course_in_question_code in courses_2a:
                correlation_check(course_in_question, semester, courses_2a)
            elif course_in_question_code in courses_2b:
                correlation_check(course_in_question, semester, courses_2b)
            elif course_in_question_code in courses_3a:
                correlation_check(course_in_question, semester, courses_3a)
            elif course_in_question_code in courses_3b:
                correlation_check(course_in_question, semester, courses_3b)
            elif course_in_question_code in courses_4a:
                correlation_check(course_in_question, semester, courses_4a)
            elif course_in_question_code in courses_4b:
                correlation_check(course_in_question, semester, courses_4b)
            else:
                continue
            
    return error

# time_slot is the [12:00,1:00]
# current_times is the times the prof is currently assigned 
# this function checks no values in time_slot overlaps with current_times
def check_overlapping_time_slot(time_slot, current_times):

    new_time_slots = [
    0,#8:30
    0,#9:00
    0,#9:30 
    0,#10:00
    0,#10:30
    0,#11:00
    0,#11:30
    0,#12:00
    0,#12:30
    0,#13:00
    0,#13:30
    0,#14:00
    0,#14:30
    0,#15:00
    0,#15:30
    0,#16:00
    0,#16:30
    0,#17:00
    0,#17:30
    0,#18:00
    0,#18:30
    0,#19:00
    0,#19:30
    0,#20:00
    0,#20:30
    0,#21:00
    0,#21:30
    0,#22:00
    ]

    # set starting time to 1
    if(time_slot[0] == '8:30'):
        new_time_slots[0] = 1
    elif(time_slot[0] == '9:00'):
        new_time_slots[1] = 1
    if(time_slot[0] == '9:30'):
        new_time_slots[2] = 1
    elif(time_slot[0] == '10:00'):
        new_time_slots[3] = 1
    if(time_slot[0] == '10:30'):
        new_time_slots[4] = 1
    elif(time_slot[0] == '11:00'):
        new_time_slots[5] = 1
    if(time_slot[0] == '11:30'):
        new_time_slots[6] = 1
    elif(time_slot[0] == '12:00'):
        new_time_slots[7] = 1
    if(time_slot[0] == '12:30'):
        new_time_slots[8] = 1
    elif(time_slot[0] == '13:00'):
        new_time_slots[9] = 1
    if(time_slot[0] == '13:30'):
        new_time_slots[10] = 1
    elif(time_slot[0] == '14:00'):
        new_time_slots[11] = 1
    if(time_slot[0] == '14:30'):
        new_time_slots[12] = 1
    elif(time_slot[0] == '15:00'):
        new_time_slots[13] = 1
    if(time_slot[0] == '15:30'):
        new_time_slots[14] = 1
    elif(time_slot[0] == '16:00'):
        new_time_slots[15] = 1
    if(time_slot[0] == '16:30'):
        new_time_slots[16] = 1
    elif(time_slot[0] == '17:00'):
        new_time_slots[17] = 1
    if(time_slot[0] == '17:30'):
        new_time_slots[18] = 1
    elif(time_slot[0] == '18:00'):
        new_time_slots[19] = 1
    if(time_slot[0] == '18:30'):
        new_time_slots[20] = 1
    elif(time_slot[0] == '19:00'):
        new_time_slots[21] = 1
    if(time_slot[0] == '19:30'):
        new_time_slots[22] = 1
    elif(time_slot[0] == '20:00'):
        new_time_slots[23] = 1
    if(time_slot[0] == '20:30'):
        new_time_slots[24] = 1
    elif(time_slot[0] == '21:00'):
        new_time_slots[25] = 1
    if(time_slot[0] == '21:30'):
        new_time_slots[26] = 1
    elif(time_slot[0] == '22:00'):
        new_time_slots[27] = 1

    # ending time to 1
    if(time_slot[1] == '8:30'):
        new_time_slots[0] = 1
    elif(time_slot[1] == '9:20'):
        new_time_slots[1] = 1
    if(time_slot[1] == '9:50'):
        new_time_slots[2] = 1
    elif(time_slot[1] == '10:20'):
        new_time_slots[3] = 1
    if(time_slot[1] == '10:50'):
        new_time_slots[4] = 1
    elif(time_slot[1] == '11:20'):
        new_time_slots[5] = 1
    if(time_slot[1] == '11:50'):
        new_time_slots[6] = 1
    elif(time_slot[1] == '12:20'):
        new_time_slots[7] = 1
    if(time_slot[1] == '12:50'):
        new_time_slots[8] = 1
    elif(time_slot[1] == '13:20'):
        new_time_slots[9] = 1
    if(time_slot[1] == '13:50'):
        new_time_slots[10] = 1
    elif(time_slot[1] == '14:20'):
        new_time_slots[11] = 1
    if(time_slot[1] == '14:50'):
        new_time_slots[12] = 1
    elif(time_slot[1] == '15:20'):
        new_time_slots[13] = 1
    if(time_slot[1] == '15:50'):
        new_time_slots[14] = 1
    elif(time_slot[1] == '16:20'):
        new_time_slots[15] = 1
    if(time_slot[1] == '16:50'):
        new_time_slots[16] = 1
    elif(time_slot[1] == '17:20'):
        new_time_slots[17] = 1
    if(time_slot[1] == '17:50'):
        new_time_slots[18] = 1
    elif(time_slot[1] == '18:20'):
        new_time_slots[19] = 1
    if(time_slot[1] == '18:50'):
        new_time_slots[20] = 1
    elif(time_slot[1] == '19:20'):
        new_time_slots[21] = 1
    if(time_slot[1] == '19:50'):
        new_time_slots[22] = 1
    elif(time_slot[1] == '20:20'):
        new_time_slots[23] = 1
    if(time_slot[1] == '20:50'):
        new_time_slots[24] = 1
    elif(time_slot[1] == '21:20'):
        new_time_slots[25] = 1
    if(time_slot[1] == '21:50'):
        new_time_slots[26] = 1
    elif(time_slot[1] == '22:20'):
        new_time_slots[27] = 1

    # fill in in-between values
    set_courses = False
    for i, val in enumerate(new_time_slots):
        # see first 1
        if val == 1 and set_courses == False:
            set_courses = True
        #in between
        elif val == 0 and set_courses == True:
            new_time_slots[i] = 1
        # see second 1 and exit
        elif val == 1 and set_courses == True:
            break
        # everything else
        else:
            pass  
    
    for i, val in enumerate(current_times):
        if current_times[i] == 1 and new_time_slots[i] == 1:
            # Oh no
            return False
        elif current_times[i] == 0 and new_time_slots[i] == 1:
            current_times[i] = 1
        elif current_times[i] == 1 and new_time_slots[i] == 0:
            pass
    return True


# check to make sure a professor is never booked to teach two courses at the same time
def check_professors_double_booked(schedule):
    errors = []
    time_slots = [
    0,#8:30
    0,#9:30 
    0,#10:00
    0,#10:30
    0,#11:00
    0,#11:30
    0,#12:00
    0,#12:30
    0,#13:00
    0,#13:30
    0,#14:00
    0,#14:30
    0,#15:00
    0,#15:30
    0,#16:00
    0,#16:30
    0,#17:00
    0,#17:30
    0,#18:00
    0,#18:30
    0,#19:00
    0,#19:30
    0,#20:00
    0,#20:30
    0,#21:00
    0,#21:30
    0,#22:00
    ]
    days_of_week = {'MONDAY': copy.deepcopy(time_slots), 'TUESDAY':copy.deepcopy(time_slots), 'WEDNESDAY':copy.deepcopy(time_slots), 'THURSDAY':copy.deepcopy(time_slots), 'FRIDAY':copy.deepcopy(time_slots)}
    semester = {"fall": copy.deepcopy(days_of_week), "spring": copy.deepcopy(days_of_week), "summer": copy.deepcopy(days_of_week)}
    professors = {}
    

    for sem in schedule:
        for course in schedule[sem]:
            section = course['sections'][0]
            prof = section['professor']['name']

            if prof not in professors:
                professors[prof] = copy.deepcopy(semester)
            timeSlots = section['timeSlots']

            for slot in timeSlots:
                scheduled_well = check_overlapping_time_slot(slot['timeRange'], professors[prof][sem][slot['dayOfWeek']])
                if scheduled_well == False:
                    msg = 'Professor {} assigned at same timeslot {} in {} on {}'.format(prof, slot['timeRange'], sem, slot['dayOfWeek'])
                    errors.append(msg)

    return errors


# check to make sure we respect a prof's requested non teaching semester
# TODO: this depends on prof type... what to do if its soft constraint not met? warning?
def check_respect_non_teaching_sem(schedule, professors):
    error = []
    # LIAM
    # prof_data = open('testing/input_professors', 'rb')
    # professors = pickle.load(prof_data)

    for semester in schedule:
        for course in schedule[semester]:
            # print(course)
            prof_key = course['sections'][0]['professor']['name']
            for prof in professors:
                if prof['name'] == prof_key:
                    if semester == prof['preferredNonTeachingSemester']:
                        error.append('{} is scheduled to teach in the {} semester, which they had requested off'.format(prof_key, semester))
    return error

# check to make sure a given course is scheduled for the required amount of hours per week based on its offering schedule
# also checks to make sure no course has more than 3 timeslots a week per section
# TODO: courses like SENG499 that are primarily lab-based might break this check. 
def check_course_time_allocation(schedule):
    error = []

    for semester in schedule:
        for course in schedule[semester]:
            for section in course['sections']:
                weekly_total = timedelta(0)
                if len(section['timeSlots']) > 3:
                    error.append('{} has more than 3 lecture slots per week in the {}.'.format(course['course']['code'], semester))
                for slot in section['timeSlots']:
                    start = datetime.strptime(slot['timeRange'][0], '%H:%M')
                    end = datetime.strptime(slot['timeRange'][1], '%H:%M')
                    daily_total = end-start
                    weekly_total += daily_total
                if weekly_total > timedelta(hours=4):
                    error.append('{} has more than 4 hours of lecture time per week in the {}.'.format(course['course']['code'], semester))
                
    return error

# check to make sure courses are scheudled within valid time ranges during the day
def check_course_times_valid(schedule):
    error = []

    for semester in schedule:
        for course_in_question in schedule[semester]:
            for section in course_in_question['sections']:
                slots = section['timeSlots']
                for slot in slots:
                    start = datetime.strptime(slot['timeRange'][0], '%H:%M')
                    end = datetime.strptime(slot['timeRange'][1], '%H:%M')

                    if start < datetime(1900, 1, 1, 8, 30):
                        error.append('{} starts too early (before 8:30AM) on {} in the {}'.format(course_in_question['course']['code'], slot['dayOfWeek'].title(), semester))
                    if end > datetime(1900, 1, 1, 22, 0):
                        error.append('{} ends too late (past 10:00PM) on {} in the {}'.format(course_in_question['course']['code'], slot['dayOfWeek'].title(), semester))
                    if start > end:
                        error.append(f"{course_in_question['course']['code']}/{semester} has an invalid time range.")

    return error


# check that all required PPW courses are present for each semester
def check_required_courses_present(schedule):
    errors = [] # this test can have multiple errors
    
    fall_courses = schedule['fall']
    spring_courses = schedule['spring']
    summer_courses = schedule['summer']

    # parse out everything thats scheduled in each semester list
    scheduled_fall_course_list = []
    scheduled_spring_course_list = []
    scheduled_summer_course_list = []

    for course in fall_courses:
        scheduled_fall_course_list.append(course['course']['code'])
    for course in spring_courses:
        scheduled_spring_course_list.append(course['course']['code'])
    for course in summer_courses:
        scheduled_summer_course_list.append(course['course']['code'])

    #TODO: what to do about the specail "OR" cases????

    # check fall
    for course in fall_course_list:
        if course not in scheduled_fall_course_list:
            
            msg = 'Required course {} missing from Fall schedule.'.format(course)
            #msg = 'fall/{}'.format(course)
            errors.append(msg)
            continue

    # check spring
    for course in spring_course_list:
        if course not in scheduled_spring_course_list:
            msg = 'Required course {} missing from Spring schedule.'.format(course)
            #msg = 'spring/{}'.format(course)
            errors.append(msg)

    # check summer
    for course in summer_course_list:
        if course not in scheduled_summer_course_list:
            msg = 'Required course {} missing from Summer schedule.'.format(course)
            #msg = 'summer/{}'.format(course)
            errors.append(msg)

    return errors



# main validate mehtod that will be imported and called by scheduler.py
def validate(schedule, professors):
    error_list = [] # empty error string to start

    error_list.extend(check_all_courses_have_section(schedule))

    error_list.extend(check_all_sections_have_timeslots(schedule))

    error_list.extend(check_all_sections_have_professor(schedule))

    error_list.extend(check_no_correlated_courses_overlap(schedule))

    error_list.extend(check_professors_double_booked(schedule))

    error_list.extend(check_respect_non_teaching_sem(schedule, professors))

    error_list.extend(check_course_time_allocation(schedule))

    error_list.extend(check_course_times_valid(schedule))

    error_list.extend(check_required_courses_present(schedule))

    return error_list


courses_1a = [
    # term 1A - FALL
    'CSC111',
    'ENGR110',
    'ENGR130',
    'MATH100', #TODO: what about courses that have "or"
    'MATH109', #TODO: what about courses that have "or"
    'MATH110',
    'PHYS110'
]

courses_1b = [
    # term 1B - SPRING
    'CSC115',
    'ENGR120',
    'ENGR141',
    'MATH101', 
    'PHYS111'
]

courses_2a = [
    # term 2A - FALL
    'ECE255', #TODO: what about courses that have "or"
    'CSC230', #TODO: what about courses that have "or"
    'CHEM101',
    'ECE260', 
    'MATH122',
    'SENG265',
    'STAT260'
]

courses_2b = [
    # term 2B - SUMMER
    'CSC225',
    'ECE310', 
    'ECON180',
    'SENG275',
    'SENG310'
]

courses_3a = [
    # term 3A - SPRING
    'ECE458', #TODO: what about courses that have "or"
    'CSC361', #TODO: what about courses that have "or"
    'CSC226',
    'ECE360',
    'SENG321',
    'SENG371'
]

courses_3b = [
    # term 3B - FALL
    'ECE355', #TODO: what about courses that have "or"
    'CSC355', #TODO: what about courses that have "or"
    'CSC320',
    'CSC360',
    'CSC370',
    'SENG350',
    'SENG360'
]

courses_4a = [
    # term 4A - SUMMER
    'SENG426',
    'SENG440', 
    'SENG499'
]

courses_4b = [
     # term 4B - SPRING
    'ECE455', #TODO: what about courses that have "or"
    'CSC460', #TODO: what about courses that have "or"
    'SENG401'
]

# master list of all courses that should be offered in a given fall semester
fall_course_list = [
    "CSC111",
    "ENGR110",
    "ENGR130",
    "MATH100", #NOTE: OR class
    "MATH109", #NOTE: OR class
    "MATH110",
    "PHYS110",
    "CSC115",
    "MATH101",
    "ECE255", #NOTE: OR class, fall should always have ECE255 at minimum instead of CSC230
    "CSC230", #NOTE: OR class, fall should always have ECE255 at minimum instead of CSC230
    "CHEM101",
    "ECE260",
    "MATH122",
    "SENG265",
    "STAT260",
    "CSC225",
    "ECON180",
    "SENG310",
    "CSC361",
    "CSC226",
    "ECE360",
    "SENG321",
    "ECE355", #NOTE: OR class, ECE355 should always be scheduled, and taken by SENG instead of CSC355
    "CSC355", #NOTE: OR class, ECE355 should always be scheduled, and taken by SENG instead of CSC355
    "CSC320",
    "CSC360",
    "CSC370",
    "SENG350",
    "SENG360"
]

# master list of all courses that should be offered in a given spring semester
spring_course_list = [
    "CSC111",
    "ENGR130",
    "MATH100", #NOTE: OR class
    "MATH109", #NOTE: OR class
    "PHYS110",
    "CSC115",
    "ENGR120",
    "ENGR141",
    "MATH101",
    "PHYS111",
    "CSC230", #NOTE: OR class
    "MATH122",
    "SENG265",
    "STAT260",
    "CSC225",
    "ECE310",
    "SENG275",
    "SENG310",
    "ECE458", #NOTE: OR class, spring should always have ECE458 instead of CSC361
    "CSC361", #NOTE: OR class, spring should always have ECE458 instead of CSC361
    "CSC226",
    "ECE360",
    "SENG321",
    "SENG371",
    "CSC320",
    "CSC360",
    "CSC370",
    "ECE455", #NOTE: OR class, ECE455 should always be available and taken instead of CSC460
    "CSC460", #NOTE: OR class, ECE455 should always be available and taken instead of CSC460
    "SENG401"
]

# master list of all courses that should be offered in a given summer semester
summer_course_list = [
    "MATH100", #NOTE: OR class
    "MATH109", #NOTE: OR class
    "CSC115",
    "ENGR141",
    "MATH101",
    "PHYS111",
    "CSC230", #NOTE: OR class
    "CHEM101",
    "ECE260",
    "MATH122",
    "SENG265",
    "STAT260",
    "CSC225",
    "ECE310",
    "ECON180",
    "SENG275",
    "SENG310",
    "CSC226",
    "CSC320",
    "CSC360",
    "CSC370",
    "SENG426",
    "SENG440",
    "SENG499"
]




