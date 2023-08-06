
import csv
import json


pengList = [
    "Adams",
    "Agathoklis",
    "Baniasadi",
    "Bhat",
    "Albu",
    "Cai" ,
    "Capson" ,
    "Darcie" ,
    "Dimopoulus",
    "Dong" ,
    "Driessen" ,
    "Gebali",
    "Gordon",
    "Gulliver" ,
    "Li",
    "Lu",
    "Lu",
    "McGuire",
    "Neville",
    "Papadopoulos",
    "Rakhmatoc",
    "Saidaminov",
    "Shuja",
    "Sima",
    "Traore",
    "Yang",
    "Damian",
    "Jackson",
    "Muller",
    "Weber",
    "Wu",
    "Zastre"
]






def createTimeRange():
    timeRanges = []

    timeRange1 = ("12:00", "13:20")
    timeRange2 = ("8:30", "10:20")
    timeRanges.append(timeRange1)
    timeRanges.append(timeRange2)

    return timeRanges


def createpreferredTimes():
    preferredTimes = {}
    preferredTimes["times"] = createTimeRange()
    preferredTimes["preferredDay"] = True

    return preferredTimes


def createAvailabilityDict():
    availabilityDict = {}

    availabilityDict["monday"] = createpreferredTimes()
    availabilityDict["tuesday"] = createpreferredTimes()
    availabilityDict["wednesday"] = createpreferredTimes()
    availabilityDict["thursday"] = createpreferredTimes()
    availabilityDict["friday"] = createpreferredTimes()

    return availabilityDict



def createSemesterAvailability():
    preferredTimes = {}
    preferredTimes["fall"] = createAvailabilityDict()
    preferredTimes["spring"] = createAvailabilityDict()
    preferredTimes["summer"] = createAvailabilityDict()

    return preferredTimes



def createCoursePreferences(courses, preferences):
    coursePreferences = []

    for c, p in zip(courses, preferences):
        coursePreference = {}
        
        if p != '0':
            coursePreference["courseCode"] = c
            coursePreference["enthusiasmScore"] = p
            coursePreferences.append(coursePreference)

    return coursePreferences

def isPeng(name):
    for prof in pengList:
        if prof in name:
            return True
    return False





def getProfessorPreferences():


    sengProfPreferencesCSV = open('../test/data/TeachPrefs_SENG499.csv')
    eceProfPreferencesCSV = open('../test/data/CSC_ECE_TeachPrefs.csv')

    sengPreferences = csv.reader(sengProfPreferencesCSV)
    sengPreferencesHeader = []
    sengPreferencesHeader = next(sengPreferences)

    ecePreferences = csv.reader(eceProfPreferencesCSV)
    ecePreferencesHeader = []
    ecePreferencesHeader = next(ecePreferences)


    Professors = []
    for row in sengPreferences:

        professor = {}

        professor["id"] = row[0]
        professor["name"] = row[0]
        professor["isPeng"] = isPeng(row[0])
        professor["facultyType"] = "Research/Teaching"
        professor["preferredTimes"] = createSemesterAvailability()

        professor["coursePreference"] = createCoursePreferences(sengPreferencesHeader[1:],row[1:])
        professor["teachingObligations"] = 6
        professor["preferredNonTeachingSemester"] = "Fall"
        Professors.append(professor)
    
    for row in ecePreferences:

        professor = {}

        professor["id"] = row[0]
        professor["name"] = row[0]
        professor["isPeng"] = isPeng(row[0])
        professor["facultyType"] = "Research/Teaching"
        professor["preferredTimes"] = createpreferredTimes()

        professor["coursePreference"] = createCoursePreferences(ecePreferencesHeader[1:],row[1:])
        professor["teachingObligations"] = 6
        professor["preferredNonTeachingSemester"] = "Fall"
        Professors.append(professor) 


    sengProfPreferencesCSV.close()
    eceProfPreferencesCSV.close()

    outdata = {
        "Professors": Professors
    }

    return outdata





#final = json.dumps(getProfessorPreferences())



#with open('../test/data/ProcessedProfessorOutput.json', 'w') as outfile:
#    outfile.write(final)



