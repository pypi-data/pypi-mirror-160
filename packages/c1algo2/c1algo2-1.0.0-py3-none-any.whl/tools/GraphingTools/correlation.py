import pickle
from statistics import correlation
from typing import OrderedDict
from sklearn.metrics import r2_score
import numpy as np
import copy


def ComputeCoeff(courses, year):
    term_comp = {}

    rev_years = {}

    for term in year:
        # reverse items in the year list to go from 2021 - 2014
        rev_years[term] = dict(reversed(list(year[term].items())))

    for term in rev_years:
        # find a correlation value for each term with each course
        # term = 1 2 2T 3 4 5 6 7
        for course in courses:
            term_comp[course] = {}
            # course = SENG440
            # courses[course] = {'2021': 99, '2020': 89, '2019': 70, '2018': 61, '2017': 50, '2016': 52, '2015': 48, '2014': 46}
            if not len(courses[course]) == len(rev_years):
                # fill_array(courses, course)
                pass
            else:
                keys = courses[course].keys()
                # r2 = r2_score([courses[course].get(x, 0) for x in keys], [rev_years[term].get(x, 0) for x in keys])
                # r2 = r2_score(list(courses[course]), list(rev_years[term]))
                r2 = np.corrcoef([courses[course].get(x, 0) for x in keys], [rev_years[term].get(x, 0) for x in keys])[0,1]
                term_comp[course][term] = r2
                print("Course = ", course, " term = ", term, " coeff = ", r2)


# def fill_array(courses, missing):
#     keys = courses[missing].keys()
#     print(keys, missing)
#     while 1:

#         pass
#     pass


def parseCourse(courseList, historical_data):

    course_enroll = {}
    fall_course_enroll = {}
    spring_course_enroll = {}
    summer_course_enroll = {}

    for course in courseList:

        course_enroll[course] = {}
        fall_course_enroll[course] = {}
        spring_course_enroll[course] = {}
        summer_course_enroll[course] = {}

        for course_banner in historical_data:

            if course == course_banner["subjectCourse"]:
                year = course_banner["term"][0:4]
                enrollment = 0
                fall_enrollment = 0
                spring_enrollment = 0
                summer_enrollment = 0
                
                if year in course_enroll[course].keys():
                    enrollment = course_enroll[course][year]

                if int(year) in range (2014, 2022):
                    enrollment += course_banner["enrollment"]
                    course_enroll[course][year] = enrollment

                    # if it is a year of interest, add the semester-wise enrollment too
                    if(course_banner['term'].endswith('09')): # fall
                        fall_enrollment = 0

                        # deals with multiple sections
                        if year in fall_course_enroll[course].keys():
                            fall_enrollment = fall_course_enroll[course][year]
                        fall_enrollment += course_banner["enrollment"]
                        fall_course_enroll[course][year] = fall_enrollment
                        
                    if(course_banner['term'].endswith('01')): # spring
                        spring_enrollment = 0
                        if year in spring_course_enroll[course].keys():
                            spring_enrollment = spring_course_enroll[course][year]
                        spring_enrollment += course_banner["enrollment"]
                        spring_course_enroll[course][year] = spring_enrollment
                    
                    if(course_banner['term'].endswith('05')): # summer
                        summer_enrollment = 0
                        if year in summer_course_enroll[course].keys():
                            summer_enrollment = summer_course_enroll[course][year]
                        summer_enrollment += course_banner["enrollment"]
                        summer_course_enroll[course][year] = summer_enrollment

    return course_enroll, fall_course_enroll, spring_course_enroll, summer_course_enroll


def parseYear(previous_enrollment):
    years = {}
    for var in previous_enrollment:
        # print(previous_enrollment[var])
        for year in previous_enrollment[var]:
            for term in previous_enrollment[var][year]:
                if not term in years.keys():
                    years[term] = {}
                years[term][year] = previous_enrollment[var][year][term] 
    return years

def get_courses(schedule):
    
    courses = []
    
    for semester in schedule:
        for course in schedule[semester]:
            capacity = course["sections"][0]["capacity"]
            if capacity in (0, None):
                courses.append(course["course"]["code"])

    courses = list(dict.fromkeys(courses))

    return courses


def main():

    # give the function banner, neville_file,
    historical_data = pickle.load(open("/Users/jay/Documents/GitHub/algorithm-2/src/tools/GraphingTools/historical_data", "rb"))
    previous_enrollment = pickle.load(open("/Users/jay/Documents/GitHub/algorithm-2/src/tools/GraphingTools/previous_enrolment", "rb"))
    schedule = pickle.load(open("/Users/jay/Documents/GitHub/algorithm-2/src/tools/GraphingTools/schedule", "rb"))

    courses = get_courses(schedule)

    years = parseYear(previous_enrollment)


    course_enroll, fall_course_enroll, spring_course_enroll, summer_course_enroll = parseCourse(courses, historical_data)

    # print("COURSE LIST", course_enroll)
    # print("FALL COURSE LIST", fall_course_enroll)
    # print("SPRING COURSE LIST", spring_course_enroll)
    # print("SUMMER COURSE LIST", summer_course_enroll)

    coeff = ComputeCoeff(course_enroll, years)
    # summer_coeff = ComputeCoeff(summer_course_enroll, years)

    # previousEnrollModification(previous_enrollment)
    # ComputeCoeff(courses, previous_enrollment, historical_data)

if __name__ == '__main__':
    main()