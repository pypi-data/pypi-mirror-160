from .course import *
import copy
from .time_slots import *
from .generate_course_list import scheduled_courses



# Input: set = list of courses to create non-conflicting subsets for
#        must_include_list = list of courses that must be included in every subset
# Output: list of all non-conflicting subsets. Eact subset contains every course in must_include_list.
# Return type: list of lists, inner lists can be empty or contain any number of course objects
def get_subsets(set, must_include_list, depth):
    # Check if empty set
    if set == []:
        return [must_include_list + []]
    # Get subsets of all elements in set excluding first
    curr_subsets = get_subsets(set[1:], must_include_list, depth)
    
    new_set = []        # List to contain new subsets (containing existing subsets joined with the first element in set
    conflict = False    # Var to check for conflicts between existing subset and first element of set

    for subset in curr_subsets:
        # Check if conflict (scheduled for same semester in reccommended schedule)
        for course in subset:
            if course.semester_conflict(set[0]):
                conflict = True
            elif course.prof_conflict(set[0]):
                conflict = True
            elif course.score_list[depth] == 0:
                conflict = True

        # Add course to new subset only if no courses in the subset conflict
        if not conflict:
            new_set.append([set[0]] + subset)
        
        conflict = False # Reset to check next subset

    # Return existing subsets concatenated with new subsets
    return curr_subsets + new_set




def update_remaining_slots(set, depth):
    must_be_children = [] # Init list of courses that must be mapped to child node time slots
    for course in set:
        #course = copy.deepcopy(course) # deepcopy so remaining slots remain the same for this course on other branches
        if course.remaining_slots == -1: 
            # first time seeing course, initialize value for how many more time slots (child nodes) are required
            if (depth <= LAST_SCHEDULABLE_TWF_SLOT):
                course.remaining_slots = 1 # TWF: requires 2 30 minutes slots, 1 remaining after this node
            elif (LAST_TWF_SLOT <= depth <= LAST_SCHEDULABLE_MTH_SLOT):
                course.remaining_slots = 2 # MTH: requires 3 30 minutes slots, 2 remaining after this node
            else:
                print("out of time slot indexes")
        else:
            course.remaining_slots = course.remaining_slots - 1 # decrease remaining time slots by one to account for this node
        if course.remaining_slots > 0:
            must_be_children.append(course) # add to must_be_children list if course requires more time slots
                                            # this course will be in all child node course sets
    # Return list of courses that must be included in child node sets
    return must_be_children



# Method removes all courses in the list 'set' from the list 'unaccounted_courses'
def update_unaccounted_courses(unaccounted_courses, set):
    for course in set:
        for unaccounted_course in unaccounted_courses:
            if unaccounted_course.name == course.name:
                unaccounted_courses.remove(unaccounted_course)
    return unaccounted_courses



# Make a node name
def make_name(node_index, set, depth, score, unaccounted_courses, all_courses_allocated, UB):
    node_name = str(node_index) + ": "
    for course in set:
        node_name += course.name + " " + "|rem.: " + str(course.remaining_slots)
    node_name += "|depth: " + str(depth) + "|score: " + str(score) + "|UB: " + str(UB)
    if depth > 26:
        node_name+="|"
        for co in unaccounted_courses:
            node_name += "+ " + co.name
    if all_courses_allocated:
        node_name += "|complete"
    return node_name



class Node_Data:

    # constructor
    def __init__(self, depth, course_set, courses_to_schedule, courses_partially_scheduled, UB, score, score_avg, complete):
        self.depth = depth
        self.course_set = course_set
        self.courses_to_schedule = courses_to_schedule
        self.courses_partially_scheduled = courses_partially_scheduled
        self.UB = UB
        self.score = score
        self.score_avg = score_avg
        self.complete = complete

    
    def get_node_average(self, new_score, num_courses):
        avg_score_touple_prev = self.score_avg
    
        if num_courses == 0:
            avg_score_touple_curr = avg_score_touple_prev
        else:
            score_prev = avg_score_touple_prev[0]
            num_courses_prev = avg_score_touple_prev[1]
            num_courses_curr = num_courses_prev + num_courses
            #print("old score: ", score_prev, ", old # courses: ", num_courses_prev, ", adding score: ", new_score)
            score_curr = ((score_prev * num_courses_prev) + new_score) / num_courses_curr
            #print("new score: ", score_curr, ", new # courses: ", num_courses_curr)
            avg_score_touple_curr = [score_curr, num_courses_curr]
        #print("avg score = ", avg_score_touple_curr[0], " (", avg_score_touple_curr[1], ")")
        return avg_score_touple_curr

