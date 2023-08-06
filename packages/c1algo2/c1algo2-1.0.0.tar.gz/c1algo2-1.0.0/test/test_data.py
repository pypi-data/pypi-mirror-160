import unittest
from c1algo2 import data
import logging
from test import io

logging.basicConfig(level=logging.WARNING)


class TestData(unittest.TestCase):

    # Set maxDiff to None for more verbose test output.
    maxDiff = None

    def generic_parse_input_test(self, test_data):
        historical_data = test_data["historical_data"]
        previous_enrollment = test_data["previous_enrollment"]
        expected_output = test_data["expected_output"]
        combined_output, training_output, testing_output = data.parse_input(historical_data, previous_enrollment)
        self.assertEqual(combined_output, expected_output)

    def test_parse_input_empty(self):
        input_data = io.load_input_pickle("empty_parse_input_test_data")
        self.generic_parse_input_test(input_data)

    def test_parse_input_small(self):
        input_data = io.load_input_pickle("small_parse_input_test_data")
        self.generic_parse_input_test(input_data)

    def test_parse_input_medium(self):
        input_data = io.load_input_pickle("medium_parse_input_test_data")
        self.generic_parse_input_test(input_data)

    def test_parse_input_large(self):
        input_data = io.load_input_pickle("large_parse_input_test_data")
        self.generic_parse_input_test(input_data)

    def generic_get_dynamic_courses_test(self, test_data):
        input_schedule = test_data["input_schedule"]
        expected_output = test_data["expected_output"]
        output = data.get_dynamic_courses(input_schedule)
        # Order doesn't matter here, so check equality with sets instead of
        # lists.
        output_set = set(output)
        expected_output_set = set(expected_output)
        self.assertEqual(output_set, expected_output_set)

    def test_get_dynamic_courses_empty(self):
        input_data = io.load_input_pickle("empty_get_dynamic_courses_test_data")
        self.generic_get_dynamic_courses_test(input_data)

    def test_get_dynamic_courses_small(self):
        input_data = io.load_input_pickle("small_get_dynamic_courses_test_data")
        self.generic_get_dynamic_courses_test(input_data)

    def test_get_dynamic_courses_medium(self):
        input_data = io.load_input_pickle("medium_get_dynamic_courses_test_data")
        self.generic_get_dynamic_courses_test(input_data)

    def test_get_dynamic_courses_large(self):
        input_data = io.load_input_pickle("large_get_dynamic_courses_test_data")
        self.generic_get_dynamic_courses_test(input_data)

    def generic_model_1_output_test(self, test_data):
        sequencer_inputs = test_data["sequencer_inputs"]
        expected_output = test_data["expected_output"]
        output = data.model_1_output(sequencer_inputs)
        self.assertEqual(output, expected_output)

    def test_model_1_output_empty(self):
        input_data = io.load_input_pickle("empty_model_1_output_test_data")
        self.generic_model_1_output_test(input_data)

    def test_model_1_output_small(self):
        input_data = io.load_input_pickle("small_model_1_output_test_data")
        self.generic_model_1_output_test(input_data)

    def test_model_1_output_medium(self):
        input_data = io.load_input_pickle("medium_model_1_output_test_data")
        self.generic_model_1_output_test(input_data)

    def test_model_1_output_large(self):
        input_data = io.load_input_pickle("large_model_1_output_test_data")
        self.generic_model_1_output_test(input_data)

    def generic_fill_capacities_test(self, test_data):
        schedule = test_data["schedule"]
        capacities = test_data["capacities"]
        expected_output = test_data["expected_output"]
        output = data.fill_capacities(schedule, capacities)
        self.assertEqual(output, expected_output)

    def test_fill_capacities_empty(self):
        input_data = io.load_input_pickle("empty_fill_capacities_test_data")
        self.generic_fill_capacities_test(input_data)

    def test_fill_capacities_small(self):
        input_data = io.load_input_pickle("small_fill_capacities_test_data")
        self.generic_fill_capacities_test(input_data)

    def test_fill_capacities_medium(self):
        input_data = io.load_input_pickle("medium_fill_capacities_test_data")
        self.generic_fill_capacities_test(input_data)

    def test_fill_capacities_large(self):
        input_data = io.load_input_pickle("large_fill_capacities_test_data")
        self.generic_fill_capacities_test(input_data)
