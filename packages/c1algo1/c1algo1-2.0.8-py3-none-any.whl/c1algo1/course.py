import json
from textwrap import indent
from .time_slots import LAST_MTH_SLOT, LAST_SCHEDULABLE_MTH_SLOT, LAST_SCHEDULABLE_TWF_SLOT, LAST_TWF_SLOT



def get_UB(score_list, depth, remaining_slots, node_index):
    if len(score_list) < 53:
        return 0

    index = depth
    max_score = 0

    while index < LAST_MTH_SLOT:
        possible_time_slot_score = 0
        if index <= LAST_SCHEDULABLE_TWF_SLOT:
            # check pairs of time slots for TWF
            if remaining_slots == 1:
                possible_time_slot_score = score_list[index]
            else:
                possible_time_slot_score = score_list[index] + score_list[index+1]
            
        elif LAST_TWF_SLOT < index <= (LAST_SCHEDULABLE_MTH_SLOT + remaining_slots):
            # check triplets of time slots for MTH

            if remaining_slots == 2:
                possible_time_slot_score = score_list[index] + score_list[index+1]
            elif remaining_slots == 1:
                possible_time_slot_score = score_list[index]
            else:
                possible_time_slot_score = score_list[index] + score_list[index+1] + score_list[index+2]

        if possible_time_slot_score > max_score:
                max_score = possible_time_slot_score

        index += 1
    
    return max_score


def get_LB(score_list, max_score):
    lowest_score = max_score
    for score in score_list:
        if 0 < score < lowest_score:
            lowest_score = score

    index = 0
    min_score = max_score
    while index < len(score_list):
        possible_time_slot_score = 0
        if index <= LAST_SCHEDULABLE_TWF_SLOT:
            # check pairs of time slots for TWF
            if score_list[index] and score_list[index+1]:
                possible_time_slot_score = score_list[index] + score_list[index+1]
            #else:
            #    possible_time_slot_score = lowest_score
            
        elif LAST_TWF_SLOT < index <= LAST_SCHEDULABLE_MTH_SLOT:
            # check triplets of time slots for MTH
            if score_list[index] and score_list[index+1] and score_list[index+2]:
                possible_time_slot_score = score_list[index] + score_list[index+1] +  score_list[index+2]
            #else:
            #    possible_time_slot_score = lowest_score
 

        if 0 < possible_time_slot_score < min_score:
                min_score = possible_time_slot_score
        
        index += 1
    
    return min_score



class Course:

 
    # constructor
    def __init__(self, name, semester, prof, time_slot_scores, season):
        self.name = name
        self.semester = semester
        self.prof = prof
        self.season = season
        self.score_list = time_slot_scores  # Must be list with size = # time slots
                                            # Each value must be between // figure this out
        self.remaining_slots = -1
        # Get maximum time slot score (calculating max score property once to speed up upper bound calculation)
        self.max_score = 0
        #(json.dumps((self.name, self.semester, self.prof, self.score_list), indent=2))

        self.max_score = get_UB(self.score_list, 0, -1, 0)
        self.min_score = get_LB(self.score_list, self.max_score)
        #print(json.dumps((self.name, self.semester, self.prof, self.score_list, self.min_score, self.max_score), indent=2))

        
        

    # Method returns True if the semesters (recommended program) are the same
    def semester_conflict(self, other_course):
        if other_course.semester == self.semester:   
            return True
        else:
            return False

    # Method returns True if the assigned professor is the same
    def prof_conflict(self, other_course):
        if other_course.prof == self.prof:   
            return True
        else:
            return False

    # Method returns the score for a time slot given it's index
    def get_score(self, time_slot_index):
        return self.score_list[time_slot_index]


