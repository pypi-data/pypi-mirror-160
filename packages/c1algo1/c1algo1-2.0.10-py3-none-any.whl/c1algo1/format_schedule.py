import copy
from .time_slots import *

class Schedule:

    def __init__(self):
        self.schedule = []

    def format_schedule(self, tree, best_index):
        # get best index node (leaf node)
        node = tree.get_node(best_index)
        # Traverse node to root to read schedule data
        while node.tag != "Root":
            # get days of week time slot is in
            node_depth = node.data.depth
            days = "TWF"
            if(LAST_TWF_SLOT < node_depth <= LAST_MTH_SLOT):
                days = "MTH"

            course_set = node.data.course_set
            for course in course_set:
                
                already_scheduled = False
                # check if already in schedule
                for scheduled_course in self.schedule:
                    if course.name == scheduled_course["name"]:
                        # update time
                        scheduled_course["start time"] = timeslots[node.data.depth%27]
                        already_scheduled = True
                if not already_scheduled:
                    # add course to schedule
                    self.schedule.append({"name": course.name, "semester": course.semester, "days": days, "start time": timeslots[node.data.depth%27], "end time": timeslots[node.data.depth%27], "season": course.season})

            node = tree.parent(node.identifier) # Get parent


    def print_schedule(self):
        print("\nSchedule:\n")
        for course in self.schedule:
            print("course: ", course["name"])
            print("semester: ", course["semester"])
            print("days: ", course["days"])
            print("start time: ", course["start time"]["start_time"])
            print("end time: ", course["end time"]["end_time"])
            print("")

    def format_output(self, input_json, season):
        json_output = copy.deepcopy(input_json)
        print("Formatting output")
        for course in self.schedule:
            for offered_course in json_output['schedule'][season]:
                if offered_course['course']['code'] == course['name']:
                    for section in offered_course['sections']:
                        if course['days'] == 'MTH':
                            section['timeSlots'].append(
                                {
                                    "dayOfWeek": "MONDAY",
                                    "timeRange": 
                                        (
                                            course['start time']['start_time'],
                                            course['end time']['end_time']
                                        )
                                }
                            )
                            section['timeSlots'].append(
                                {
                                    "dayOfWeek": "THURSDAY",
                                    "timeRange":
                                        (
                                            course['start time']['start_time'],
                                            course['end time']['end_time']
                                        )
                                }
                            )
                        else:
                            section['timeSlots'].append(
                                {
                                    "dayOfWeek": "TUESDAY",
                                    "timeRange":
                                        (
                                            course['start time']['start_time'],
                                            course['end time']['end_time']
                                        )
                                }
                            )
                            section['timeSlots'].append(
                                {
                                    "dayOfWeek": "WEDNESDAY",
                                    "timeRange": 
                                        (
                                            course['start time']['start_time'],
                                            course['end time']['end_time']
                                        )
                                }
                            )
                            section['timeSlots'].append(
                                {
                                    "dayOfWeek": "FRIDAY",
                                    "timeRange": 
                                        (
                                            course['start time']['start_time'],
                                            course['end time']['end_time']
                                        )
                                }
                            )
        
        #json_output.pop('professors')                    
        return json_output
