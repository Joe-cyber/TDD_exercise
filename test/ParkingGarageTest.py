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

    def test_park_one_occupied(self):
        garage = ParkingGarage()
        occupied = garage.check_occupancy(ParkingGarage.INFRARED_PIN1)
        self.assertTrue(occupied)
