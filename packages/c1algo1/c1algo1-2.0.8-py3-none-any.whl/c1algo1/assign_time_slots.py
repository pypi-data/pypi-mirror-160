from treelib import Tree, Node   # Library for tree data structure
from .time_slots import *        # Defines list of time slots
from .bounding import *          # Provides functions for calculation upper and lower bounds
from .format_schedule import *   # Provides functions for formating the schedule list and printing its data
from .node_data import *         # Provides object for data stored at each node
from time import *
import copy, sys
from .generate_course_list import scheduled_courses


# Define a maximum number of nodes to expand at each level in the tree
MAX_NUM_CHILD_NODES = 3

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def assign_time_slots(course_list, season):
    # Init tree data structure
    tree = Tree()

    # Init best lower bound
    best_lower_bound = 0

    best_score = 0      # highest score of node with all courses in branch scheduled
    best_index = 0      # index of node with all courses in branch scheduled with highest score
    
    # Inite best score average
    highest_score_avg = 0

    # Get all subsets of all non-conflicting courses
    all_subsets = get_subsets(course_list, [], 0)
    subsets = all_subsets

    # Add root to tree and node list
    node_data = Node_Data(-1, [], course_list, [], 0, 0, [0, 0], False)
    node_list = [tree.create_node(tag="Root", identifier=0, data=node_data) ]
    node = node_list[0]

    # Init child node list to keep track of nodes to expand at each level in tree
    child_node_list = []


    # Init depth and index variables for each node
    depth = 0
    node_index = 1

    num_nodes_to_filter = 0

    # while there are still possible child nodes to create and their depth does not surpass the # of time slots
    while(len(node_list)>0 and depth<=LAST_MTH_SLOT):
        # Iterate subsets of non-conflicting courses that can be mapped to the time slot (depth) in the current branch
        for set in subsets:

            set = copy.deepcopy(set)
        
            # Get child node depth (time slot #) by incrementing current node depth
            depth = node.data.depth + 1
            # only continue if there are enough time slots for this depth
            if(depth<LAST_MTH_SLOT and not node.data.complete):

                # Remove any course in current set from list of unaccounted courses
                unaccounted_courses = copy.deepcopy(node.data.courses_to_schedule) # Get current list of unaccounted courses from node
                unaccounted_courses = update_unaccounted_courses(unaccounted_courses, set) # Update list for child node

                # Update each course's # of remaining slots property, get list of courses that have remaining time slots
                child_node_courses = update_remaining_slots(set, depth)

                # Get node score of parent node
                score = node.data.score
                # Add time slot score for each score in current subset to score
                for course in set:
                    score += course.get_score(depth)
                
                # Get upper and lower bounds
                UB = score + get_max_scores(unaccounted_courses+child_node_courses, depth, node.identifier)
                LB = score + get_min_scores(unaccounted_courses)


                # Only create child node if best possible score is better then least worst case
                if(UB >= best_lower_bound):

                    # Update best lower bound if LB is greater
                    if LB > best_lower_bound:
                        best_lower_bound = LB

                    # Check if all courses have been scheduled (for full duration) in branch
                    all_courses_allocated = False
                    if len(unaccounted_courses)==0 and len(child_node_courses)==0:
                        all_courses_allocated = True
                        for course in set:
                            if course.remaining_slots>0: 
                                all_courses_allocated = False # update to false if any courses still require more time slots

                    # Save index if the score is the highest score and all courses have been scheduled in branch
                    if score > best_score and all_courses_allocated:
                        best_score = score
                        best_index = node_index

                    # Make a node name
                    node_name =  make_name(node_index, set, depth, score, unaccounted_courses, all_courses_allocated, UB)

                    # Get score average
                    temp_score = 0
                    for course in set:
                        temp_score += course.get_score(depth)

                    score_avg = node.data.get_node_average(temp_score, len(set))

                    if score_avg[0] > highest_score_avg:
                        highest_score_avg = score_avg[0]

                    score_avg = copy.deepcopy(node.data.score_avg)
                    score_avg[1] += len(set)
                    score_avg[0] = ((score + UB) / 2)


                    # Format node data
                    node_data = Node_Data(depth, set, unaccounted_courses, child_node_courses, UB, score, score_avg, all_courses_allocated)

                    # Add child node to tree and to list of potential nodes to expand and sort by score average
                    child_node_list.append(tree.create_node(tag=node_name, identifier=node_index, data=node_data, parent=node.identifier))
                    child_node_list = sorted(child_node_list, key=lambda child_node: child_node.data.score_avg[0], reverse=True)

                    num_nodes_to_filter += 1
                    
                    node_index += 1



        # Remove node from list of nodes to expand
        node_list.remove(node)

        # Check if out of nodes to expand on this level
        if(len(node_list)==0):

            child_node_list = child_node_list[0:MAX_NUM_CHILD_NODES]

            #print("Level ", depth, " complete")
            #print("# of nodes created: ", num_nodes_to_filter)
            num_nodes_to_filter = 0

            if len(child_node_list) == 0:
                #print("Tree reached depth of ", depth)
                break   # break if there are no more nodes to expand

            # copy child node list to node list to expand as reset child node list to empty list
            node_list = child_node_list
            child_node_list = []
        

        # Toggle brute force vs branch and bound
        brute_force = False
        if (brute_force):
            # First just try getting the highest scoring child node
            max_node = Node(data=Node_Data(-1, -1, -1, -1, -1, -1))
            for n in tree.children(node.identifier):
                if (n.data.score > max_node.data.score):
                    max_node = n
            node = max_node
        else:
            # Get node with highest score from node list to expand
            node = node_list[0]
            for n in node_list:
                if n.data.score > node.data.score:
                    node = n


        must_include = node.data.courses_partially_scheduled # courses in node set that require more time slots (must be included in all child nodes)
        depth = node.data.depth + 1
        # only consider unaccounted courses if there is enough time slots left in day to fit it in:
        if(LAST_SCHEDULABLE_TWF_SLOT < depth <= LAST_TWF_SLOT):
            subsets = get_subsets(must_include, [], depth)

        elif(LAST_SCHEDULABLE_MTH_SLOT < depth <= LAST_MTH_SLOT):
            subsets = get_subsets(must_include, [], depth)

        else:
            unaccounted = node.data.courses_to_schedule # courses not yet scheduled in branch
            # get all non-conflicting subsets of unaccounted courses that contain all courses in must_include
            courses_to_consider = []
            for uc in unaccounted:
                if uc.get_score(depth) > 0:
                    courses_to_consider.append(uc)

            # check conflict with course alredy scheduled (based on consistency in historical offerings)
            for scheduled_course in scheduled_courses[season][depth]:
                set_index = 0
                #print("\ncomparing ", scheduled_course.name, "_", scheduled_course.semester, "(", scheduled_course.prof[4:8], ")", end=" with ")
                while set_index < len(courses_to_consider):
                    course = courses_to_consider[set_index]
                    #print(course.name, "-", course.semester, "(", course.prof[4:8], ")", end=",  ")
                    if course.semester_conflict(scheduled_course) or course.prof_conflict(scheduled_course):
                        courses_to_consider.remove(course)
                    else:
                        set_index += 1
                
            subsets = get_subsets(courses_to_consider, must_include, depth)


    #tree.show()
    #print("best score: ", best_score)

    # Format schedule
    schedule = Schedule()
    schedule.format_schedule(tree, best_index)
    return schedule



def assign_times(course_list, input_json, season):

    # remove courses with no prof from course_list
    index = 0
    while(index < len(course_list)):
        course = course_list[index]
        if course.prof is None:
            course_list.remove(course)
            #print("Removing ", course.name)
        
        else:
            index += 1

    # # of courses to schedule
    COURSE_CAPACITY = len(course_list)


    # Temporary: Update MTH scores since 2/3 as many MTH slots as TWF slots are required
    for course in course_list:
        score_index = 0
        while(score_index < len(course.score_list)):
            if score_index >= 27:
                course.score_list[score_index] = course.score_list[score_index] * 3/2 
            score_index += 1

    # For development: print input list of course objects, manually update time scores
    '''#print("list:")
    for course in course_list[0:COURSE_CAPACITY]:
        print("\r")
        print("course: ", course.name)
        #print("semester:", course.semester)
        #print("prof: ", course.prof)
        print("time slot scores: ", end="")
        index = 0
        while index < len(course.score_list):
            if( index==27 ): print("|")
            # Force CSC320 and SENG321 to be schduled in MTH slots
            if (course.name == "CSC320" and 28 < index < 34):
                pass
                #course.score_list[index] = 5 
            if (course.name == "ECE360" and 36 < index < 41):
                pass
                #course.score_list[index] = 20
            s = course.score_list[index]
            print(s, end=", ")
            index += 1
        print("\r")
    print("\n")'''


    start_time = time()

    eprint("\t- Running branch and bound algorithm to assign time slots with {} courses.".format(COURSE_CAPACITY))
    eprint("\t- Maximum # of tree levels is 54.")
    eprint("\t- Maximum number of nodes being expanded at each level is {}.".format(MAX_NUM_CHILD_NODES))

    schedule = assign_time_slots(course_list[0:COURSE_CAPACITY], season) # run course to time slots branch and bound

    end_time = time()
    print("Time slot assignment complete in {} seconds".format(round((end_time-start_time), 2)))


    # Print schedule
    #print_schedule()
    #print("Total # of nodes: ", number_of_nodes)


    return schedule.format_output(input_json, season)