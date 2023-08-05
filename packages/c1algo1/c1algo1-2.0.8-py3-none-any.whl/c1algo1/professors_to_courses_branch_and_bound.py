import copy, timeit
from treelib import Node, Tree
from .scheduler_tools import associate_profs_with_courses, sort_courses_by_prof_interest

# BEGIN CLASS DEFINITIONS

class Professor():
    def __init__(self, id, name, preference, workload, preferredSemesterOff):
        self.id = id
        self.name = name
        self.preference = preference
        self.workload = workload
        self.preferredSemesterOff = preferredSemesterOff

    def __repr__(self) -> str:
        return self.name # + ' ' + str(self.preference) + ' ' + str(self.workload)

class Course():
    def __init__(self, code, professors, semester):
        self.code = code
        self.professors = professors
        self.semester = semester

    def __repr__(self) -> str:
        return self.code + '/' + self.semester #+ '\n' + str(self.professors)

class NodeData():
    def __init__(self, courses, cost, course, assigned_prof, leaf=False):
        self.courses = courses
        self.cost = cost
        self.course = course
        self.assigned_prof = assigned_prof
        self.leaf = leaf

# END CLASS DEFINITIONS

# BEGIN HELPER FUNCTIONS #

# Parses the input JSON to produce a list of courses for a given year
# Returns: A list of Course objects
# If no year is provided, it will parse the 'schedule' portion of the JSON I.E. the new schedule
# If a year is provided, it will parse the 'historicalData' section of the JSON for that year
# TODO: Remove code reuse
def generate_courses_list(input_sorted_by_prof_interest, historical_year=None):
    courses = []
    if historical_year is None: 
        for semester in input_sorted_by_prof_interest['schedule']:
            for course in input_sorted_by_prof_interest['schedule'][semester]:            
                code = course['course']['code']
                professors = []            
                for prof_id, preference in course['interestedProfs'].items():
                    if preference < 1:
                        continue
                    workload = 0
                    name = ''
                    preferredSemesterOff = ''
                    for temp_p in input_sorted_by_prof_interest['professors']:
                        if temp_p['id'] == prof_id:
                            workload = temp_p['teachingObligations']  
                            name = temp_p['name']
                            preferredSemesterOff = temp_p['preferredNonTeachingSemester']
                    professors.append(Professor(prof_id, name, preference, workload, preferredSemesterOff))
                professors = sorted(professors, key=lambda prof: prof.preference, reverse=True)
                courses.append(Course(code, professors, semester))
    else:
        for semester in input_sorted_by_prof_interest['historicalData'][historical_year]:
            for course in input_sorted_by_prof_interest['historicalData'][historical_year][semester]:        
                code = course['course']['code']
                professors = []            
                for prof_id, preference in course['interestedProfs'].items():
                    workload = 0
                    name = ''
                    for temp_p in input_sorted_by_prof_interest['professors']:
                        if temp_p['id'] == prof_id:
                            workload = temp_p['teachingObligations']
                            name = temp_p['name']
                    professors.append(Professor(prof_id, name, preference, workload))
                courses.append(Course(code, professors, semester))
    return sorted(courses, key=lambda course: (len(course.professors), sum([prof.preference for prof in course.professors])))
# END HELPER FUNCTIONS #


# Use branch and bound to find solution(s) for assigning professors to courses for a given year
# Returns: A list of solutions to assigning professors to courses. These are copies of the JSON input with the 'professor' field of each course section filled, one JSON per solution found
# Only assigns professors to courses which have interested professors
# If no year is provided, solutions are applied to the 'schedule' portion of the JSON I.E. the new schedule
# If a year is provided, solutions are applied to the 'historicalData' section of the JSON for that year
# TODO: Optimize pruning and branching so that more than 1 solution can be found in feasible time
# TODO: Add error-handling
# TODO: Remove print statements when they are no longer useful
# TODO: Overall code review for code optimizations
def assign_profs_to_courses_branch_and_bound(input_sorted_by_prof_interest, historical_year=None):   

    start = timeit.default_timer()

    # Get courses into a nice readable format
    courses = generate_courses_list(input_sorted_by_prof_interest, historical_year)

    # Separate out the courses with no profs able to be assigned
    unassigned = [course for course in courses if len(course.professors) == 0]
    courses = [course for course in courses if course not in unassigned]

    print(f"Found prof preferences for {len(courses)}/{len(courses) + len(unassigned)} courses")
    print('unassigned courses: {}'.format(unassigned))

    # Setup our tree
    upper_bound = float('inf')
    tree = Tree()
    root = Node('Root', 'root', data=NodeData(courses, cost=0, course=None, assigned_prof=None))
    tree.add_node(root)
    solutions = []

    # Starting from the root
    current_node = tree.get_node('root')
    solution_limit = 1
    i = 1
    print('Limiting output to ' + str(solution_limit) + ' solutions')
    while current_node is not None:

        # Check for "leaf" (i.e. no more courses left to assign) (there will be other actual leaf nodes but if they still have courses it just means they haven't been explored yet)
        if len(current_node.data.courses) == 0:
            
            # Mark the node as a leaf so we stop looking at it later
            current_node.data.leaf = True

            # If we found a tie for best cost, add it to a list of potential solutions
            if current_node.data.cost == upper_bound:
                solutions.append(current_node)

            # Otherwise, check if we've got a new best cost
            if current_node.data.cost < upper_bound:
                upper_bound = current_node.data.cost

                # if we assigned a new best cost, traverse the tree and prune branches
                for node in tree.all_nodes():
                    if node.data.cost > upper_bound:
                        tree.remove_node(node.identifier)

                # Prune the list of solutions
                solutions = [node for node in solutions if node.data.cost <= upper_bound]

                # Add this new best cost to our list of solutions
                solutions.append(current_node)

                print('Solution found, cost: ' + str(current_node.data.cost))
                
            # Impose some arbitrary limit on the number of solutions to present so that we don't endlessly spin when the input data is too easy
            if len(solutions) >= solution_limit:
                break
        else:
            # Get the first course in the list from the current node
            course = current_node.data.courses.pop(0)
            
            # Remove empty workload profs
            course.professors = [professor for professor in course.professors if professor.workload > 0]

            if len(course.professors) == 0:
                unassigned.append(course)
                print(f"{course.code}/{course.semester} could not be assigned")

            # If there is a prof(s) with 195 for this course we should only look at those
            zero_cost_profs = [professor for professor in course.professors if professor.preference == 195]
            if len(zero_cost_profs) > 0:
                course.professors = zero_cost_profs

            # Branch for each choice
            for professor in course.professors:                
                
                # Calculate the cost to get to this node so far
                # Preference gets cut in half if its during a preferred non-teaching semester
                if course.semester == professor.preferredSemesterOff:
                    professor.preference *= 0.5
                new_cost = current_node.data.cost + (195 - professor.preference)

                # if this next choice would cost more than our current upper bound, don't bother exploring it
                if new_cost > upper_bound:
                    continue
                
                # Copy over the remaining courses
                new_courses = copy.deepcopy(current_node.data.courses) # deepcopy is used so that changes we make in other branches don't affect this one (at the cost of memory)
                
                # Subtract 1 course from the professors workload in all other courses
                for temp_course in new_courses:
                    for temp_professor in temp_course.professors:
                        if temp_professor.name == professor.name:
                            temp_professor.workload = temp_professor.workload - 1                
                
                new_node = Node(tag=course.code + professor.name, data=NodeData(courses=new_courses, cost=new_cost, course=course, assigned_prof=professor))
                tree.add_node(new_node, parent=current_node)

        # Move to the least cost node (now we look at actual leaves)
        least_cost = float('inf')
        next_node = None

        # if we haven't found a solution yet, go to the cheapest of the current nodes children so we can hit a leaf as fast as possible
        if len(solutions) == 0:
            for child in tree.children(current_node.identifier):
                if child.data.cost < least_cost:
                    least_cost = child.data.cost
                    next_node = child

        # if we didn't find a naive solution, just check for the lowest leaf anywhere
        else:
            if next_node is None:
                leaves = [leaf for leaf in tree.leaves() if leaf.data.leaf is False]
            for leaf in leaves:
                if leaf.data.cost < least_cost:
                    least_cost = leaf.data.cost
                    next_node = leaf

        current_node = next_node

        #print('Nodes Processed: ' + str(i), end='\r')
        #print('Assigned ' + current_node.data.assigned_prof.name + ' to ' + current_node.data.course.code + '/' + current_node.data.course.semester)
        i = i + 1
    
    #print('Formatting Output.......')
    #tree.show(filter = lambda node: node.data.cost == upper_bound and (len(tree.is_branch(node.identifier)) > 0 or tree.depth(node.identifier) == tree.depth()), data_property='assigned_prof')
    #tree.show(data_property='assigned_prof')
    prof_course_assignments = []
    for solution in solutions:
        assignment_set = []
        temp_curr = solution
        while not temp_curr.is_root():
            assignment_set.append((temp_curr.data.assigned_prof, temp_curr.data.course))
            temp_curr = tree.parent(temp_curr.identifier)
        prof_course_assignments.append(assignment_set)
        print('Solution ' + str(len(prof_course_assignments)) + ' assigned ' + str(len(assignment_set)) + ' professors.')

    
    #print(prof_course_assignments)

    all_inputs_with_assigned_profs = []
    for assignment_set in prof_course_assignments:
        single_input_with_assigned_profs = send_output_to_json(assignment_set, input_sorted_by_prof_interest, historical_year, unassigned)
        all_inputs_with_assigned_profs.append(single_input_with_assigned_profs)
    
    stop = timeit.default_timer()
    print('Generated ' + str(len(prof_course_assignments)) + ' solutions in ' + str(round((stop-start), 2)) + 's')
    
    return all_inputs_with_assigned_profs

# Takes a list of tuples: (professor, course) and assigns the professor to that course in the json_input
# Returns: the JSON input with the 'professor' member of each section filled
# Only applies to assignable courses that had interested professors
# If no year is provided, solutions are applied to the 'schedule' portion of the JSON I.E. the new schedule
# If a year is provided, solutions are applied to the 'historicalData' section of the JSON for that year
# TODO: Properly handle multiple sections rather than assigning the same professor to all of them
def send_output_to_json(prof_course_assignment, json_input, historical_year, unassigned_courses):
    json_output = copy.deepcopy(json_input)
    for assignment in prof_course_assignment:
        professor_object = assignment[0]
        course_object = assignment[1]

        if historical_year is None:
            for course in json_output['schedule'][course_object.semester]:
                if course['course']['code'] == course_object.code:
                    if (len(course['sections']) > 0):
                        for section in course['sections']:
                            section['professor'] = {'id': professor_object.id, 'name': professor_object.name}
                    else:
                        course['sections'].append({
                            'professor': {'id': professor_object.id, 'name': professor_object.name},
                            'timeSlots': []
                            });
                    course.pop('interestedProfs')
        else:
            for course in json_output['historicalData'][historical_year][course_object.semester]:
                if course['course']['code'] == course_object.code:
                    if (len(course['sections']) > 0):
                        for section in course['sections']:
                            section['professor'] = {'id': professor_object.id, 'name': professor_object.name}
                    else:
                        course['sections'].append({
                            'professor': {'id': professor_object.id, 'name': professor_object.name},
                            'timeSlots': []
                            });
                    course.pop('interestedProfs')
    
    # Remove unassigned courses from the output
    for course_object in unassigned_courses:
        if historical_year is None:
            for i, course in enumerate(json_output['schedule'][course_object.semester]):
                if course['course']['code'] == course_object.code:
                    # Get rid of interestedProfs
                    course.pop('interestedProfs')
                    # Make sure its not a pre-assigned course like chem 101
                    if len(course['sections']) > 0:
                        num_sections = len(course['sections'])
                        num_assigned_profs = len([section['professor'] for section in course['sections'] if section['professor'] is not None])
                        num_assigned_timeslots = len([section['timeSlots'] for section in course['sections'] if len(section['timeSlots']) > 0])
                        if num_assigned_profs == num_sections and num_assigned_timeslots == num_sections:
                            # Every sectiion has a prof assigned and a set of timeSlots so we don't want to pop it from our output
                            continue
                    json_output['schedule'][course_object.semester].pop(i)
        else:
            for i, course in enumerate(json_output['historicalData'][historical_year][course_object.semester]):
                if course['course']['code'] == course_object.code:
                    # Get rid of interestedProfs
                    course.pop('interestedProfs')
                    # Make sure its not a pre-assigned course like chem 101
                    if len(course['sections']) > 0:
                        num_sections = len(course['sections'])
                        num_assigned_profs = len([section['professor'] for section in course['sections'] if section['professor'] is not None])
                        num_assigned_timeslots = len([section['timeSlots'] for section in course['sections'] if len(section['timeSlots']) > 0])
                        if num_assigned_profs == num_sections and num_assigned_timeslots == num_sections:
                            # Every sectiion has a prof assigned and a set of timeSlots so we don't want to pop it from our output
                            continue
                    json_output['schedule'][course_object.semester].pop(i)

    return json_output
        


# main runner for testing
def generate_partial_schedule(scheduler_input, historical_year=None):

    print('Preprocessing.......')
    # first, we want to associate professors with courses
    input_with_interested_profs = associate_profs_with_courses(scheduler_input, historical_year)

    # second, we want to rank these courses in ascending order with respect to how many professors
    # indicated they had a > 0 preference value in teaching it. 
    input_sorted_by_prof_interest = sort_courses_by_prof_interest(input_with_interested_profs, historical_year)

    # call method to assign profs to each course
    all_inputs_with_assigned_profs = assign_profs_to_courses_branch_and_bound(input_sorted_by_prof_interest, historical_year)

    return all_inputs_with_assigned_profs # final partial schedule
