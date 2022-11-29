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
    def setUp(self) -> None:
        self.pg = ParkingGarage()

    @patch.object(GPIO, 'input')
    def test_park_one_occupied(self, mock_input):
        mock_input.return_value = 50
        occupied = self.pg.check_occupancy(ParkingGarage.INFRARED_PIN1)
        self.assertTrue(occupied)

    @patch.object(GPIO, 'input')
    def test_park_one_not_occupied(self, mock_input):
        mock_input.return_value = 0
        occupied = self.pg.check_occupancy(ParkingGarage.INFRARED_PIN1)
        self.assertFalse(occupied)
