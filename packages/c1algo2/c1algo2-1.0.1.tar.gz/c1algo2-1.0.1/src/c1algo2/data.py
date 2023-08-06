import copy
import random
import logging
import math
import numpy as np
from collections import defaultdict

MONTH_TO_SEMESTER = {
    "09": "Fall",
    "01": "Spring",
    "05": "Summer"
}

SHADOWS = {
    "ECE255": "CSC230",
    "ECE458": "CSC361",
    "ECE355": "CSC355",
    "ECE455": "CSC460"
}

# Inverse of SHADOWS
SHADOWED_BY = {SHADOWS[course]: course for course in SHADOWS}


def parse_input(historical_data: dict, previous_enrollment: dict) -> tuple([dict, dict]):
    # Outermost:    Dictionary, where keys are courses e.g. "CSC111" and values
    #               are dicts.
    # Each dict within a course contains the following structure:
    # {
    #   "CSCS111": {
    #       "2008":
    #           {
    #               "1": 10,
    #               "2": 10,
    #               "2T": 10,
    #               "3": 10,
    #               "4": 10,
    #               "5": 10,
    #               "6": 10,
    #               "7": 10,
    #               "Fall_Enrollment": 50,
    #               "Fall_MaxEnrollment": 60,
    #               "Spring_Enrollment": 50,
    #               "Spring_MaxEnrollment": 60,
    #               "Summer_Enrollment": 50,
    #               "Summer_MaxEnrollment": 60
    #           }
    #   }
    # }
    # course{year{term{section{}}}}

    final_input = {}

    for course in historical_data:
        offering = f"""{course["subject"]}{course["courseNumber"]}"""

        if course['term'].endswith('09'):
            year = course["term"][0:4]
        else:
            # Convert str to int, subtract 1, convert back to str.
            year = str(int(course["term"][0:4]) - 1)
        term = course['term'][-2:]
        # "Fall", "Spring" or "Summer"
        term = MONTH_TO_SEMESTER[term]

        # if the course is already in the dictionary, just append data to that
        # key
        if offering not in final_input:
            final_input[offering] = {}
        # if the course is new, add as a new key
        if year not in final_input[offering]:
            final_input[offering][year] = {}
        final_input[offering][year].setdefault(f"{term}_Enrollment", 0)
        final_input[offering][year].setdefault(f"{term}_MaxEnrollment", 0)
        final_input[offering][year][f"{term}_Enrollment"] += course["enrollment"]
        final_input[offering][year][f"{term}_MaxEnrollment"] += course["maximumEnrollment"]

        final_input[offering][year].update(get_enrollment_by_year(previous_enrollment, year))

    training_input = {}
    testing_input = {}

    training_years = []

    earliest_year, latest_year = get_earliest_and_latest_year(final_input)

    for year in range(earliest_year, latest_year):          # Skip last entry, as latest year must be part of testing data
        if random.random() <= 0.75:                         # 75% chance to put input into training set
            training_years.append(str(year))                # If it isn't a training year, then it must be a testing year

    for course in final_input:
        training_input[course] = {}
        testing_input[course] = {}
        for year in final_input[course]:
            if year in training_years:
                training_input[course][year] = final_input[course][year]
            else:
                testing_input[course][year] = final_input[course][year]

    return final_input, training_input, testing_input


def get_earliest_and_latest_year(final_input: dict) -> tuple([int, int]):
    latest_year = 0
    earliest_year = 10000

    for course in final_input:
        for year in final_input[course]:
            if int(year) > latest_year:
                latest_year = int(year)
            elif int(year) < earliest_year:
                earliest_year = int(year)

    return earliest_year, latest_year


def round_floats_to_ints(float_list: list) -> list:
    int_list = []
    # If the list is more than 1-dimensional, run this function recursively on each list.
    if float_list.ndim > 1:
        for float_sublist in float_list:
            int_list.append(round_floats_to_ints(float_sublist))
    # Otherwise, run this function on each float in the list.
    else:
        for float_value in float_list:
            int_value = round(float_value)
            int_list.append(int_value)
    return int_list


# TODO: I think this is including chem, math phys etc... should we change that?
def get_dynamic_courses(schedule: dict):

    courses = []

    for semester in schedule:
        for course in schedule[semester]:
            capacity = course["sections"][0]["capacity"]
            if capacity in (0, None):
                courses.append(course["course"]["code"])

    courses = list(dict.fromkeys(courses))

    return courses


def get_enrollment_by_year(enrollment_data: dict, year: str) -> dict:
    if year in enrollment_data:
        return enrollment_data[year]
    else:
        return {
            "1": 0,
            "2": 0,
            "2T": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0
        }


# TODO: Consider making `input_file` a more descriptive argument name.
def model_1_output(input_file: dict) -> dict:
    # use deepcopy to change iterable objects in the dictionary
    output = copy.deepcopy(input_file)
    for course in output:
        for year in output[course]:
            output[course][year]["Year_Enrollment"] = 0
            output[course][year]["Year_MaxEnrollment"] = 0

            for term in ("Fall", "Spring", "Summer"):
                if f"{term}_Enrollment" in output[course][year]:
                    output[course][year]["Year_Enrollment"] += output[course][year][f"{term}_Enrollment"]
                    output[course][year]["Year_MaxEnrollment"] += output[course][year][f"{term}_MaxEnrollment"]
                    output[course][year].pop(f"{term}_Enrollment")
                    output[course][year].pop(f"{term}_MaxEnrollment")

    return output


# This is not ugly anymore, its brother is though.
def fill_capacities(schedule: dict, capacities: dict) -> dict:
    SEMESTERS = (
        (0, "fall"),
        (1, "spring"),
        (2, "summer")
    )

    # Copy the schedule dict for filling.
    final_schedule = copy.deepcopy(schedule)

    # Create a copy that we can mutate. We empty this as we populate capacities
    # into the schedule object.
    capacities = copy.deepcopy(capacities)

    # Get ONE instance of an offering for each course. We will need much of
    # this information to add new offerings.
    offering_prototype = {}
    for semester in final_schedule:
        offering_prototype.update({offering["course"]["code"]: offering for offering in final_schedule[semester]})

    # Update sections for required offerings.
    # For each semester:
    for semester_index, semester in SEMESTERS:
        # For each offering in the schedule object:
        for offering in final_schedule[semester]:
            isCSC = offering["course"]["code"].startswith("CSC")
            isECE = offering["course"]["code"].startswith("ECE")
            isSENG = offering["course"]["code"].startswith("SENG")

            if not isCSC and not isECE and not isSENG:
                continue

            course_code = offering["course"]["code"]
            capacity = capacities[course_code][semester_index]
            # We sized and the schedule has this course in the current semester, so we just fill.
            if capacity is not None:
                num_sections = len(offering["sections"])
                offering["sections"] = sections(course_code, capacity, num_sections)
                capacities[course_code][semester_index] = None
                logging.debug(
                    f"""Required offering of {course_code} in the {semester} contains
                    {len(offering["sections"])} sections with capacities
                    {[section["capacity"] for section in offering["sections"]]}."""
                )
            # We did NOT size the course for this semester, but it is required in the schedule.
            else:
                num_sections = len(offering["sections"])
                offering["sections"] = sections(course_code, 100, num_sections)
                capacities[course_code][semester_index] = None
                logging.debug(
                    f"""Required offering of {course_code} in the {semester} contains
                    {len(offering["sections"])} sections with capacities
                    {[section["capacity"] for section in offering["sections"]]}."""
                )
    # Add sections for new offerings.
    for semester_index, semester in SEMESTERS:
        for course_code in capacities:
            if capacities[course_code][semester_index] is not None:
                capacity = capacities[course_code][semester_index]
                new_offering = copy.deepcopy(offering_prototype[course_code])
                num_sections = len(new_offering["sections"])
                new_offering["sections"] = sections(course_code, capacity, num_sections)
                final_schedule[semester].append(new_offering)
                capacities[course_code][semester_index] = None
                logging.debug(
                    f"""New offering of {course_code} in the {semester} contains
                    {len(offering["sections"])} sections with capacities
                    {[section["capacity"] for section in offering["sections"]]}."""
                )

    return final_schedule


def section(capacity: int) -> dict:
    return {
        "professor": None,
        "capacity": capacity,
        "timeSlots": []
    }


def sections(course_code: str, total_capacity: int, num_sections: int) -> list[dict]:
    if num_sections == 1:
        return [section(total_capacity)]
    # ECE: 25% to A01, 75% to A02
    elif num_sections == 2 and course_code[:3] == "ECE":
        a01_capacity = math.ceil(total_capacity * 0.25)
        a02_capacity = math.floor(total_capacity * 0.75)
    # CSC/SENG: 75% to A01, 25% to A02
    else:  # CSC/SENG course with 2 sections.
        a01_capacity = math.floor(total_capacity * 0.75)
        a02_capacity = math.ceil(total_capacity * 0.25)

    return [section(a01_capacity), section(a02_capacity)]


def extrapolate_list_maker(year_s_previous_enrollment: dict) -> list:
    year_standing_list = []
    for year in year_s_previous_enrollment:
        year_standing_list.append(year_s_previous_enrollment[year])
    return year_standing_list


def extrapolate_values(switched_dict: dict) -> dict:
    final_standings_dict = {}
    for year_standing in switched_dict:
        final_years_dict = {}
        year_standing_list = extrapolate_list_maker(switched_dict[year_standing])
        years = list(range(2014, 2022))
        fit = np.polyfit(years, year_standing_list, 1)
        line = np.poly1d(fit)
        new_years = list(range(2008, 2014))
        extra_data = round_floats_to_ints(line(new_years))
        new_data = [0 if i < 0 else i for i in extra_data]
        for entry in year_standing_list:
            new_data.append(entry)
        for entry in years:
            new_years.append(entry)
        for year, value in zip(new_years, new_data):
            final_years_dict[year] = value
        final_standings_dict[year_standing] = final_years_dict
    return final_standings_dict


def nested_dict_switcher(old_dict: dict) -> dict:
    switched_dict = defaultdict(dict)
    for k, v in old_dict.items():
        for k2, v2 in v.items():
            switched_dict[k2][k] = v2
    new_dict = dict(switched_dict)
    return new_dict


def extrapolate_prev_enrollment(previous_enrollment: dict) -> dict:
    switched_dict = nested_dict_switcher(previous_enrollment)
    result = extrapolate_values(switched_dict)
    unswitched_dict = nested_dict_switcher(result)

    return unswitched_dict
