import json, datetime
from tracemalloc import start
from c1algo1.course import Course

def assign_courses_from_historical_offering(courses_and_profs):

    with open("./historical-data/courses_with_common_times.json", "r") as fh:
        courses_by_semester = json.load(fh)

    with open("./c1algo1/data/input/SENG_PPW.json", "r") as fh:
        seng_ppw = json.load(fh)

    for sem in courses_by_semester:
        for course in courses_by_semester[sem]:
            consecutive_offerings = courses_by_semester[sem][course][1]
            if consecutive_offerings > 3:

                pref_timeslots = {}

                try:
                    onstream_sem = seng_ppw[course]['OnstreamSemester']
                except:
                    continue

                for semester in courses_and_profs['schedule']:
                    for key in courses_and_profs['schedule'][semester]:
                        match_course = key['course']['code']
                        prof = key['sections'][0]['professor']

                        if course == match_course and sem == semester:

                            monday_thursday = [0] * 27
                            tuesday_wednesday_friday = [0] * 27

                            start_time = datetime.datetime.strptime(str(courses_by_semester[sem][course][0][0]), "%H:%M")
                            end_time = datetime.datetime.strptime(str(courses_by_semester[sem][course][0][1]), "%H:%M")
                            day_spread = courses_by_semester[sem][course][0][2]


                            base_time = datetime.datetime(1900, 1, 1)

                             # Converting Start Time / End Time into index 

                            min_to_start = (start_time - base_time).total_seconds() / 60 
                            min_to_end = (end_time - base_time).total_seconds() / 60 

                            # Subtract BASE Minutes (830 AM = 510minutes, divide by 30 to get starting index)
                            starting_index = int((min_to_start - 510) / 30)

                            # Subtract BASE Minutes by 500 (As END TIME IS NOT a multiple of 30 (10 minutes less) and divide by 30 to get ending index)
                            ending_index= int((min_to_end - 500) / 30)

                            for i in range(starting_index, ending_index):

                                if day_spread == 'MTh':
                                    monday_thursday[i] = 10
                                if day_spread == 'TWF':
                                    tuesday_wednesday_friday[i] = 10

                            pref_timeslots['monday_thursday'] = monday_thursday
                            pref_timeslots['tuesday_wednesday_friday'] = tuesday_wednesday_friday
                            
                            print(json.dumps((course,prof,onstream_sem,pref_timeslots), indent=2))
                            print("---" * 50)
                