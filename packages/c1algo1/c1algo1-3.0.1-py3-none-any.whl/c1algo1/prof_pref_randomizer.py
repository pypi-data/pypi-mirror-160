import json
import random

time_slots = ['8:30',
'9:00',
'9:30',
'10:00',
'10:30',
'11:00',
'11:30',
'12:30',
'13:00',
'13:30',
'14:00',
'14:30',
'15:00',
'15:30',
'16:00',
'16:30',
'17:00',
'17:30',
'18:00',
'18:30',
'19:00',
'19:30',
'20:00',
'20:30',
]#22 start values

enthusiasm_scores = [0, 20, 39, 40, 78, 100, 195]

non_teaching_semester = ['FALL', 'SPRING', 'SUMMER']

course_day_spread = ['TWF', 'MTh'] #ignoring individual days of the week here



def get_faculty_type(is_teaching):
    if(is_teaching):
        return 'TEACHING'
    else:
        return 'RESEARCH'


def get_randomized_time_ranges():
    time_range = []
    range_start = 0 # 8:30
    range_end = 22 # 20:30
    end_of_start_times = 20 # 7:00, last time class should ever START
    max_time_range = random.randint(1, 3) # how many different time ranges will the prof give
    range_counter = 0
    while(range_start <= end_of_start_times and range_counter < max_time_range):
        # try to push the starting values earlier to make it more realistic
        earliest_start_time_list = [random.randint(range_start, end_of_start_times), random.randint(range_start, end_of_start_times), random.randint(range_start, end_of_start_times)]
        start_time = min(earliest_start_time_list)
        end_time = random.randint(start_time+2, range_end)

        time_range.append((time_slots[start_time], time_slots[end_time]))
        range_start = end_time + 1
        range_counter += 1
        
    # get anything that slips through the cracks
    if len(time_range) == 0:
        time_range.append((time_slots[range_start], time_slots[range_end]))
    
    return time_range

def get_course_preferences(is_peng):
    course_preferences = []
    file = open('../data/input/all_courses.json')
    all_courses = json.load(file)
    for c in all_courses:
        #randomly make it so most course have 0's and dont get added to prof, probably a better way to do this
        enter = [random.randint(0, 6), random.randint(0, 6), random.randint(0, 6), random.randint(0, 6), random.randint(0, 6), random.randint(0, 6), random.randint(0, 6)]
        if(0 not in enter):
            enthusiasm_score_index = random.randint(1, 6)
            preference = {}
            preference['courseCode'] = c['course_code']
            preference['enthusiasmScore'] = enthusiasm_scores[enthusiasm_score_index]
            course_preferences.append(preference)
    return course_preferences

    
def get_day_times():
    day_times = {}
    day_times['monday'] = get_randomized_time_ranges()
    day_times['tuesday'] = get_randomized_time_ranges()
    day_times['wednesday'] = get_randomized_time_ranges()
    day_times['thursday'] = get_randomized_time_ranges()
    day_times['friday'] = get_randomized_time_ranges()
    return day_times

def get_preferred_times():
    preferred_times = {}
    preferred_times['fall'] = get_day_times()
    preferred_times['spring'] = get_day_times()
    preferred_times['summer'] = get_day_times()
    return preferred_times

def get_teaching_obligations(faculty_type):
    if(faculty_type == 'TEACHING'):
        return 6
    else:
        return 3

def get_preferred_non_teaching_semester():
    return non_teaching_semester[random.randint(0, 2)]

def get_preferred_course_day_spread():
    return course_day_spread[random.randint(0, 1)]


def get_randomized_professors():

    f = open('../data/input/all_professors.json')

    print("loading data document")
    all_professors = json.load(f)

    print("done loading data...")

    professors = []

    for obj in all_professors:
        prof = {}
        prof['id'] = obj['id']
        prof['name'] = obj['first_name'] + obj['last_name']
        prof['isPeng'] = obj['is_peng']
        prof['facultyType'] = get_faculty_type(obj['is_teaching'])
        prof['preferredTimes'] = get_preferred_times()
        prof['coursePreferences'] = get_course_preferences(obj['is_peng'])
        prof['teachingObligations'] = get_teaching_obligations(prof['facultyType'])
        prof['preferredNonTeachingSemester'] = get_preferred_non_teaching_semester()
        prof['preferredCourseDaySpreads'] = get_preferred_course_day_spread()

        professors.append(prof)
        final_file = {}
        final_file['professors'] = professors
        final = json.dumps(final_file)
        #print(final)
        with open('randomized_professors.json', 'w') as outfile:
            outfile.write(final)



# for standalone testing
if __name__ == "__main__":
    get_randomized_professors()
