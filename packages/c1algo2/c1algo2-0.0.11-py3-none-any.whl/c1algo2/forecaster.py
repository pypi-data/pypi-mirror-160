import numpy as np
from sklearn.linear_model import LinearRegression
from c1algo2 import data, evaluator
import logging


def create_model_1_input(model_1_input: dict) -> tuple([dict, dict]):
    """Creates Model_1_input (ALl Courses) Object which initializes formats model 1 input data
    """
    x_years = {}
    y_enrollments = {}
    for course in model_1_input:
        x_years[course], y_enrollments[course] = create_model_1_course(model_1_input[course])
    return x_years, y_enrollments


def create_model_1_course(course: dict) -> tuple([np.array, np.array]):
    """Creates Model_1_input (1 course)
    """
    x_year = []  # x_year[i] = course[year].key()[ij] (year i, semester j)
    y_enrollment = []  # y_enrollment[i] = course[year][semester]["maximumEnrollment"]
    for i_year in course:
        x_year.append(int(i_year))
        y_enrollment.append(int(course[i_year]["Year_MaxEnrollment"]))
    x_year = np.array(x_year, dtype=np.int32).reshape(-1, 1)
    y_enrollment = np.array(y_enrollment, dtype=np.int32)
    return x_year, y_enrollment


def create_model_2_input(model_2_input: dict) -> tuple([dict, dict]):
    """Creates Model_2_input (All courses) object which formats model 2 input per course
    """
    x = {}
    y = {}
    for course in model_2_input:
        x[course], y[course] = create_model_2_course(model_2_input[course])
    return x, y


def create_model_2_course(course: dict) -> tuple([np.array, np.array]):
    """creates Model_2_input (1 course)
    """
    x_year_enrollment = []
    y_semesters = []

    for year in course:
        enrollment_for_year = 0
        enrollment = [0, 0, 0]
        if year in course.keys():
            if "Fall_MaxEnrollment" in course[year]:
                enrollment[0] = course[year]["Fall_MaxEnrollment"]
                enrollment_for_year += course[year]["Fall_MaxEnrollment"]
            if "Spring_MaxEnrollment" in course[year]:
                enrollment[1] = course[year]["Spring_MaxEnrollment"]
                enrollment_for_year += course[year]["Spring_MaxEnrollment"]
            if "Summer_MaxEnrollment" in course[year]:
                enrollment[2] = course[year]["Summer_MaxEnrollment"]
                enrollment_for_year += course[year]["Summer_MaxEnrollment"]

        x_year_enrollment.append([year, enrollment_for_year])
        y_semesters.append(enrollment)

    x_year_enrollment = np.array(x_year_enrollment, dtype=np.int32)
    y_semesters = np.array(y_semesters, dtype=np.int32)
    return x_year_enrollment, y_semesters


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


def normalize_output(output):
    for course in output:
        max_value = max(output[course])
        # Remove negative values.
        output[course] = [max(0, i) for i in output[course]]
        # Remove all values lower than the square root of the max value. This
        # is to eliminate "close to 0 but not quite" errors. Potential errors
        # here: e.g. what if 5 students do a project in 1 semester, but only 1
        # in another?
        output[course] = [0 if i < max_value**(1/2) else i for i in output[course]]
        # Set values of 0 to None.
        output[course] = [None if i == 0 else i for i in output[course]]


def forecast(historical_data, previous_enrollment, schedule, verbose=False):

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    (
        sequencer_combined_inputs,
        sequencer_training_inputs,
        sequencer_testing_inputs
    ) = data.parse_input(historical_data, previous_enrollment)
    sizer_training_inputs = data.model_1_output(sequencer_training_inputs)
    sizer_testing_inputs = data.model_1_output(sequencer_testing_inputs)

    courses = data.get_dynamic_courses(schedule)

    sizer = LinearRegression()
    sequencer = LinearRegression()

    x_years_training, y_enrollments_training = create_model_1_input(sizer_training_inputs)
    x_year_enrollment_training, y_semesters_training = create_model_2_input(sequencer_training_inputs)

    x_years_testing, y_enrollments_testing = create_model_1_input(sizer_testing_inputs)
    x_year_enrollment_testing, y_semesters_testing = create_model_2_input(sequencer_testing_inputs)

    size_output_dict = {}
    size_testing_dict = {}

    sequence_output_dict = {}
    sequence_testing_dict = {}

    for course in courses:
        sizer.fit(x_years_training[course], y_enrollments_training[course])
        sequencer.fit(x_year_enrollment_training[course], y_semesters_training[course])
        y1_pred_floats = sizer.predict(x_year_enrollment_testing[course][:, 0].reshape(-1, 1))
        y1_pred = np.array(round_floats_to_ints(y1_pred_floats), dtype=np.int32)
        # This is currently only doing predictions for 1 year
        x_2 = [np.array([x_year_enrollment_training[course][:, 0][0], y1_pred[0]]).transpose()]
        y2_pred_floats = sequencer.predict(x_2)
        y2_pred = round_floats_to_ints(y2_pred_floats)

        size_output_dict[course] = y1_pred[0]
        size_testing_dict[course] = y_enrollments_testing[course][0]
        sequence_testing_dict[course] = y_semesters_testing[course][0]
        sequence_output_dict[course] = y2_pred[0]

        logging.debug("    **** " + str(course) + " Predicted Sequencing ****")
        for input, pred in zip(x_year_enrollment_training[course], y2_pred):
            logging.debug("Year: " + str(int(input[0])) + "     Size: " + str(int(input[1])) + "    Prediction:" + str(pred))

    sizer_rating = evaluator.sizer_score(size_output_dict, size_testing_dict)
    sequencer_rating = evaluator.sequencer_score(sequence_output_dict, sequence_testing_dict)

    logging.debug(sizer_rating)
    logging.debug(sequencer_rating)

    normalize_output(sequence_output_dict)

    schedule = data.fill_capacities(schedule, sequence_output_dict)

    logging.info(sequence_output_dict)

    return schedule
