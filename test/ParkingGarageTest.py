import unittest
from unittest.mock import patch

from ParkingGarage import ParkingGarage
from ParkingGarageError import ParkingGarageError

import mock.GPIO as GPIO
from mock.RTC import RTC


class ParkingGarageTest(unittest.TestCase):
    """
    Your test methods go here
    """
    @patch.object(GPIO, 'input')
    def test_park_one_occupied(self, mock_input):
        garage = ParkingGarage()
        mock_input.return_value = 50
        occupied = garage.check_occupancy(ParkingGarage.INFRARED_PIN1)
        self.assertTrue(occupied)


