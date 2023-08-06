# sorts a list of courses by number of professors willing to teach them (ascending order)
def sort_courses_by_prof_interest(input_with_interested_profs, historical_year=None):

    if historical_year is None:
        # pull out the schedule as we only want to sort this key of the larger dict
        schedule = input_with_interested_profs['schedule']

        # sort each sem and then re-insert sorted sem into schedule
        for sem in schedule:
            sorted_list = sorted(schedule[sem], key=lambda x: (len(x['interestedProfs'].items()), sum(x['interestedProfs'].values())))
            schedule[sem] = sorted_list
        input_with_interested_profs['schedule'] = schedule
    else:
        # pull out the schedule as we only want to sort this key of the larger dict
        schedule = input_with_interested_profs['historicalData'][historical_year]

        # sort each sem and then re-insert sorted sem into schedule
        for sem in schedule:
            sorted_list = sorted(schedule[sem], key=lambda x: (len(x['interestedProfs'].items()), sum(x['interestedProfs'].values())))
            schedule[sem] = sorted_list
        input_with_interested_profs['historicalData'][historical_year] = schedule

    return input_with_interested_profs

# associates professors with courses that they are potentially interested in teaching
def associate_profs_with_courses(scheduler_input, historical_year=None):

    # Add empty interestedProfs to each course
    for semester in scheduler_input['schedule']:
        for course in scheduler_input['schedule'][semester]:
            course['interestedProfs'] = {}
   

    for prof in scheduler_input['professors']:
        pEng = prof['isPeng']

        # Only look at semesters where the prof wants to teach (hard constraint for research profs only)
        if prof['facultyType'] == 'RESEARCH':
            teachingSemesters = [semester.lower() for semester in ['FALL', 'SPRING', 'SUMMER'] if semester != prof['preferredNonTeachingSemester']]
        else:
            teachingSemesters = ['fall', 'spring', 'summer']
        
        for coursePreference in prof['coursePreferences']:
            code = coursePreference['courseCode'].replace(" ", "")
            score = coursePreference['enthusiasmScore']

            # Don't add profs who's preference is 0
            if score <= 0:
                continue

            if historical_year is None:
                for semester in teachingSemesters:
                    for course in scheduler_input['schedule'][semester]:
                        # If we find the course and the professor meets the ppEng requirements, add the prof to list of intersted profs
                        if (course['course']['code'] == code) and (course['course']['pengRequired'][semester] == pEng):
                            course['interestedProfs'][prof['id']] = score
            else:
                for semester in teachingSemesters:
                    for course in scheduler_input['historicalData'][historical_year][semester]:
                        if (course['course']['code'] == code) and (course['course']['pengRequired'][semester] == pEng):
                            course['interestedProfs'][prof['id']] = score
            
    return scheduler_input                   