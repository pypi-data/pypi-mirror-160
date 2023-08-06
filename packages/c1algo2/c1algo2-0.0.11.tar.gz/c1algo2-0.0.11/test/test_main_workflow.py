import unittest

from c1algo2 import forecaster
from test import io


class TestMainWorkflow(unittest.TestCase):

    def test_main_workflow(self):

        # Load the backend data.
        historical_data, previous_enrolment, schedule = io.load_backend_inputs()
        forecaster.forecast(historical_data, previous_enrolment, schedule)
