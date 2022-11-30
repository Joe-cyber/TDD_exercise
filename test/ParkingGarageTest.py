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

    @patch.object(RTC, 'get_current_time_string')
    def test_calculate_parking_fee_one_hour(self, mock_input):
        mock_input.return_value = "12:30:00"
        fee = self.pg.calculate_parking_fee("12:00:00")
        self.assertEqual(2.50, fee)

    @patch.object(RTC, 'get_current_time_string')
    def test_calculate_parking_fee_two_hour(self, mock_input):
        mock_input.return_value = "13:30:00"
        fee = self.pg.calculate_parking_fee("12:00:00")
        self.assertEqual(5.0, fee)

    @patch.object(RTC, 'get_current_time_string')
    def test_calculate_parking_fee_three_hour(self, mock_input):
        mock_input.return_value = "13:30:00"
        fee = self.pg.calculate_parking_fee("11:00:00")
        self.assertEqual(7.5, fee)

    @patch.object(RTC, 'get_current_time_string')
    @patch.object(RTC, 'get_current_day')
    def test_calculate_parking_fee_three_hour_on_week_end(self, mock_input, mock_input2):
        mock_input2.return_value = "13:30:00"
        mock_input.return_value = "SATURDAY"
        fee = self.pg.calculate_parking_fee("11:00:00")
        self.assertEqual(9.38, fee)

    def test_servo_open(self):
        self.pg.open_garage_door()
        open = self.pg.is_open()
        self.assertIsNotNone(open)
        self.assertTrue(open)

    def test_servo_closed(self):
        self.pg.close_garage_door()
        open = self.pg.is_open()
        self.assertIsNotNone(open)
        self.assertFalse(open)

    def test_light_on(self):
        self.pg.turn_light_on()
        on = self.pg.light_is_on()
        self.assertIsNotNone(on)
        self.assertTrue(on)
