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

    @patch.object(GPIO, 'input')
    def test_get_occupied_spots_three(self, mock_input):
        mock_input.side_effect = [50, 50, 50]
        occupied = self.pg.get_occupied_spots()
        self.assertEqual(3, occupied)

    @patch.object(GPIO, 'input')
    def test_get_occupied_spots_zero(self, mock_input):
        mock_input.side_effect = [0, 0, 0]
        occupied = self.pg.get_occupied_spots()
        self.assertEqual(0, occupied)

    @patch.object(GPIO, 'input')
    def test_get_occupied_spots_two(self, mock_input):
        mock_input.side_effect = [50, 0, 50]
        occupied = self.pg.get_occupied_spots()
        self.assertEqual(2, occupied)

    @patch.object(GPIO, 'input')
    def test_calculate_parking_fee_one_hour(self, mock_input):
        mock_input.return_value = "12:00:00"
        fee = self.pg.calculate_parking_fee("12:30:00")
        self.assertEqual(2.50, fee)

