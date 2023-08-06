import datetime, json, timeit, sys
from .generate_course_list import generate_course_list
import os
from .scheduler_tools import associate_profs_with_courses, sort_courses_by_prof_interest
from .assign_time_slots import assign_times
from .professors_to_courses_branch_and_bound import assign_profs_to_courses_branch_and_bound
from .validator import validate

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# here we will take the sorted course dict and assign professors to each course.
def assign_profs_to_courses(input_sorted_by_prof_interest):

    professors = input_sorted_by_prof_interest['professors']


    for current_semester in input_sorted_by_prof_interest['schedule']:
        for course in input_sorted_by_prof_interest['schedule'][current_semester]:
            highest_pref = 0
            assigned_prof = None
            if len(course['interestedProfs'].items()) == 0:
                # TODO : Properly assign no prof to course. (NEW FORMAT)
                course['sections'].append({
                    'professor' :  None,
                    'timeSlots': []
                })
                continue

            for professor, preference in course['interestedProfs'].items():
                search = next((i for i, prof in enumerate(professors) if prof['id'] == professor), None)
                if search == None:
                    print('prof not found.')
                    continue
                if professors[search]['teachingObligations'] == 0:
                    continue
                if professors[search]['preferredNonTeachingSemester'] == current_semester.upper():
                    continue
                # TODO: check profs preference for class size?
                if preference > highest_pref:
                    highest_pref = preference
                    assigned_prof = professor

            search = next((i for i, prof in enumerate(professors) if prof['id'] == assigned_prof), None)

            professors[search]['teachingObligations'] = professors[search]['teachingObligations'] - 1
            

            search = next((i for i, offered_course in enumerate(input_sorted_by_prof_interest['schedule'][current_semester]) if offered_course['course']['code'] == course['course']['code']), None)

            # print(input_sorted_by_prof_interest['schedule'][current_semester][search]['assignedProfessor'])
            input_sorted_by_prof_interest['schedule'][current_semester][search]['sections'].append({
                    'professor' :  assigned_prof,
                    'timeSlots': []
                })


    return input_sorted_by_prof_interest

def assign_courses_to_timeslots(courses_and_timeslots):

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './data/input/correlated_courses.json')

    with open(filename, "r") as fh:
        corellated_courses_list = json.load(fh)

    # retrieve list of correlated courses by on stream semester offering

    for current_semester in courses_and_timeslots['schedule']:

        monday_thursday = [[] for _ in range(27)]
        tuesday_wednesday_friday = [[] for _ in range(27)]
        base_time = 510
        curr_day = 0

        for course in courses_and_timeslots['schedule'][current_semester]:
            key = course['course']['code']
            correlated_courses_for_key = corellated_courses_list[current_semester][key]['CorrelatedCourses']
            # Unneeded In Output
            course.pop('interestedProfs')

            #TODO : Add in edge case where one day is full - should not occur but IF monday fills up
            #TODO : When a time is assigned, ADD THAT TIME TO DAY for Professor blacklist time
            #TODO : Check that the current time you are scheduling does not fall within Prof Blacklist Time.
            
            for i in range(27):

                # Monday Thursday

                if curr_day % 5 == 1 or 4:
                    if len(monday_thursday[i]) == 0 and len(monday_thursday[i+1]) == 0 and len(monday_thursday[i+2]) == 0:
                        monday_thursday[i].append(key)
                        monday_thursday[i+1].append(key)
                        monday_thursday[i+2].append(key)
                        start_time = datetime.timedelta(minutes=(base_time + (i * 30)))
                        end_time = datetime.timedelta(minutes=(base_time - 10 + ((i+3) * 30)))
                        
                        search = next((i for i, offered_course in enumerate(courses_and_timeslots['schedule'][current_semester]) if offered_course['course']['code'] == key), None)

                        slots = [
                            {
                                'dayOfWeek' : 'MONDAY', 
                                'timeRange' : [(str(start_time), str(end_time))]
                            }, 
                            {
                                'dayOfWeek' : 'THURSDAY' , 
                                'timeRange' : [(str(start_time), str(end_time))]
                            }
                        ]

                        for timeslot in slots:
                            courses_and_timeslots['schedule'][current_semester][search]['sections'][0]['timeSlots'].append(timeslot)
  
                        curr_day +=1
                        break
                    else:
                        does_not_correlate = True
                        for j in range(3):
                            for item in monday_thursday[i + j]:
                                if item in correlated_courses_for_key:
                                    does_not_correlate = False
                                    break
                            # if item not in correllated_courses:
                        if does_not_correlate:     
                            monday_thursday[i].append(key)
                            monday_thursday[i+1].append(key)
                            monday_thursday[i+2].append(key)
                            start_time = datetime.timedelta(minutes=(base_time + (i * 30)))
                            end_time = datetime.timedelta(minutes=(base_time - 10 + ((i+3) * 30)))
                            
                            search = next((i for i, offered_course in enumerate(courses_and_timeslots['schedule'][current_semester]) if offered_course['course']['code'] == key), None)

                            slots = [
                                {
                                    'dayOfWeek' : 'MONDAY', 
                                    'timeRange' : [(str(start_time), str(end_time))]
                                }, 
                                {
                                    'dayOfWeek' : 'THURSDAY' , 
                                    'timeRange' : [(str(start_time), str(end_time))]
                                }
                            ]

                            for timeslot in slots:
                                courses_and_timeslots['schedule'][current_semester][search]['sections'][0]['timeSlots'].append(timeslot)

                            curr_day +=1
                            break

                # Tuesday Wednesday Friday Scheduler

                if curr_day % 5 == 2 or 3 or 5:

                    if len(tuesday_wednesday_friday[i]) == 0 and len(tuesday_wednesday_friday[i+1]) == 0:
                        tuesday_wednesday_friday[i].append(key)
                        tuesday_wednesday_friday[i+1].append(key)

                        start_time = datetime.timedelta(minutes=(base_time + (i * 30)))
                        end_time = datetime.timedelta(minutes=(base_time - 10 + ((i+2) * 30)))

                        search = next((i for i, offered_course in enumerate(courses_and_timeslots['schedule'][current_semester]) if offered_course['course']['code'] == key), None)

                        slots = [
                             {
                                'dayOfWeek' : 'TUESDAY', 
                                'timeRange' : [(str(start_time), str(end_time))]
                            }, 
                            {
                                'dayOfWeek' : 'WEDNESDAY' , 
                                'timeRange' : [(str(start_time), str(end_time))]
                            }, 
                            {
                                'dayOfWeek' : 'FRIDAY' , 
                                'timeRange' : [(str(start_time), str(end_time))]
                            }
                        ]

                        for timeslot in slots:
                            courses_and_timeslots['schedule'][current_semester][search]['sections'][0]['timeSlots'].append(timeslot)

                        curr_day +=1
                        break

                    else:
                        does_not_correlate = True
                        for j in range(2):
                            for item in monday_thursday[i + j]:
                                if item in correlated_courses_for_key:
                                    does_not_correlate = False
                                    break
                        if does_not_correlate:
                            tuesday_wednesday_friday[i].append(key)
                            tuesday_wednesday_friday[i+1].append(key)

                            start_time = datetime.timedelta(minutes=(base_time + (i * 30)))
                            end_time = datetime.timedelta(minutes=(base_time - 10 + ((i+2) * 30)))

                            search = next((i for i, offered_course in enumerate(courses_and_timeslots['schedule'][current_semester]) if offered_course['course']['code'] == key), None)


                            slots = [
                                {
                                    'dayOfWeek' : 'TUESDAY', 
                                    'timeRange' : [(str(start_time), str(end_time))]
                                }, 
                                {
                                    'dayOfWeek' : 'WEDNESDAY' , 
                                    'timeRange' : [(str(start_time), str(end_time))]
                                }, 
                                {
                                    'dayOfWeek' : 'FRIDAY' , 
                                    'timeRange' : [(str(start_time), str(end_time))]
                                }
                            ]

                            for timeslot in slots:
                                courses_and_timeslots['schedule'][current_semester][search]['sections'][0]['timeSlots'].append(timeslot)

                            curr_day +=1
                            break
                    
    return courses_and_timeslots


# singular method imported and called by backend to generate a schedule
def generate_schedule(professors, schedule):

    scheduler_input = {
        "professors": None,
        "schedule": None
    }
    scheduler_input['professors'] = professors
    scheduler_input['schedule'] = schedule

    with open ('./schedule.json', 'w+') as output:
        json.dump(scheduler_input['schedule'], output, indent=2)

    error = "" # error string as defined in spec

    eprint("------ START ALGO 1 ------")
    start = timeit.default_timer()
    # Check for professors that have no preferences
    no_prefs = []
    for prof in scheduler_input['professors']:
        if sum([pref['enthusiasmScore'] for pref in prof['coursePreferences']]) == 0:
            no_prefs.append(prof['name'])
    if no_prefs:
        error = f"The following profs failed to submit preferences: {no_prefs}"

    # first, we want to associate professors with courses
    input_with_interested_profs = associate_profs_with_courses(scheduler_input)

    # second, we want to rank these courses in ascending order with respect to how many professors
    # indicated they had a > 0 preference value in teaching it. 
    input_sorted_by_prof_interest = sort_courses_by_prof_interest(input_with_interested_profs)

    # call method to assign profs to each course
    profs_associated_with_courses = assign_profs_to_courses_branch_and_bound(input_sorted_by_prof_interest)

    courses_and_timeslots_class_list = generate_course_list(profs_associated_with_courses[0])

    fall_course_list = courses_and_timeslots_class_list[1]
    spring_course_list = courses_and_timeslots_class_list[2]
    summer_course_list = courses_and_timeslots_class_list[3]

    # call method to assign courses to timeslots based on output of previous step for fall
    eprint("\nScheduling {} courses for the fall semester".format(len(fall_course_list)))
    courses_and_timeslots = assign_times(fall_course_list, profs_associated_with_courses[0], "fall")

    # call method to assign courses to timeslots based on output of previous step for spring
    eprint("\nScheduling {} courses for the spring semester".format(len(spring_course_list)))
    courses_and_timeslots = assign_times(spring_course_list, courses_and_timeslots, "spring")

    # call method to assign courses to timeslots based on output of previous step for summer
    eprint("\nScheduling {} courses for the summer semester".format(len(summer_course_list)))
    courses_and_timeslots = assign_times(summer_course_list, courses_and_timeslots, "summer")

    courses_and_timeslots.pop('professors')

    stop = timeit.default_timer()
    eprint('\nGenerated schedule in {}s'.format(round((stop-start), 2)))

    eprint("------ END ALGO 1 ------")

    return courses_and_timeslots['schedule'], error # final schedule and error if any

# validate a a given course schedule
# returns list of issues
def validate_schedule(schedule, professors):

    errors = validate(schedule, professors)

    return errors



