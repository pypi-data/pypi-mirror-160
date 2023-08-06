import unittest
from c1algo2 import forecaster
from test import io
import logging

logging.basicConfig(level=logging.WARNING)


class TestForecaster(unittest.TestCase):

    def test_dynamic_course_presence(self):

        # Load the backend data.
        historical_data, previous_enrolment, schedule = io.load_backend_inputs()

        # Register all dynamic courses in the backend input schedule.
        input_dynamic_courses = {}
        for semester in schedule:
            for course in schedule[semester]:
                # If the course is a dynamic course:
                capacity = course["sections"][0]["capacity"]
                if capacity in (0, None):
                    # Register the course in `input_courses`.
                    course_code = course["course"]["code"]
                    input_dynamic_courses[course_code] = True

        output_schedule = forecaster.forecast(historical_data, previous_enrolment, schedule, verbose=False)

        # Register all courses in the output schedule.
        output_courses = {}
        for semester in output_schedule:
            for course in output_schedule[semester]:
                # All courses here are dynamic courses.
                course_code = course["course"]["code"]
                output_courses[course_code] = True

        for input_dynamic_course in input_dynamic_courses:
            self.assertIn(input_dynamic_course, output_courses)
