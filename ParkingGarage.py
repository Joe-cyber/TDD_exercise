import time
import mock.GPIO as GPIO
from mock.RTC import RTC
from ParkingGarageError import ParkingGarageError
from datetime import datetime


class ParkingGarage:
    # Pin number declarations
    INFRARED_PIN1 = 11
    INFRARED_PIN2 = 12
    INFRARED_PIN3 = 13
    RTC_PIN = 15
    SERVO_PIN = 16
    LED_PIN = 18

    def __init__(self):
        """
        Constructor
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.INFRARED_PIN1, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN2, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN3, GPIO.IN)
        GPIO.setup(self.RTC_PIN, GPIO.IN)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        self.rtc = RTC(self.RTC_PIN)
        self.pwm = GPIO.PWM(self.SERVO_PIN, 50)
        self.pwm.start(0)
        self.servo_status = None
        self.light_on = None

    def check_occupancy(self, pin: int) -> bool:
        """
        Checks whether one of the infrared distance sensor detects something in front of it.
        :param pin: The data pin of the sensor that is being checked (e.g., INFRARED_PIN1).
        :return: True if the infrared sensor detects something, False otherwise.
        """
        if pin in [self.INFRARED_PIN1, self.INFRARED_PIN2, self.INFRARED_PIN3]:
            occupied = GPIO.input(pin)
            if occupied > 0:
                return True
            return False
        else:
            raise ParkingGarageError

    def get_occupied_spots(self) -> int:
        """
        Calculates the number of occupied parking spots in the garage.
        :return: The number of occupied spots.
        """
        occupied = [self.check_occupancy(p) for p in [self.INFRARED_PIN1, self.INFRARED_PIN2, self.INFRARED_PIN3]]
        return occupied.count(True)

    def calculate_parking_fee(self, entry_time: str) -> float:
        """
        Uses the RTC to calculate the amount of money to be paid by the customer of the garage
        For each hour spent in the garage, there is a flat cost of 2.50 €;
        additionally, during the weekend (Saturday and Sunday)
        an additional 25% fee is applied to the total of the parking ticket.
        Even when customers do not exceed a full hour, they will still be charged 2.50 €.
        :param entry_time: A string in the format "hh:mm:ss" containing the entry time of a
        vehicle in the garage
        :return: The total amount to be paid by the customer
        """
        actual_time = datetime.strptime(RTC.get_current_time_string(), "%H:%M:%S")
        entry_time = datetime.strptime(entry_time, "%H:%M:%S")
        hours = actual_time - entry_time
        hours = int(hours.seconds / (60 * 60)) + 1
        price = hours * 2.50
        return round(price, 2) if RTC.get_current_day() != "SATURDAY" and RTC.get_current_day() != "SUNDAY" else round(
            (price + price * 0.25), 2)

    def open_garage_door(self) -> None:
        """
        Opens the garage door using the servo motor
        A motor angle of 180 degrees corresponds to a fully open door
        """
        self.servo_status = True
        self.change_servo_angle(180)

    def close_garage_door(self) -> None:
        """
        Closes the garage door using the servo motor
        A motor angle of 0 degrees corresponds to a fully closed door
        """
        self.servo_status = False
        self.change_servo_angle(0)

    def turn_light_on(self) -> None:
        """
        Turns on the smart lightbulb
        """
        GPIO.output(self.LED_PIN, GPIO.HIGH)
        self.light_on = True

    def turn_light_off(self) -> None:
        """
        Turns off the smart lightbulb
        """
        GPIO.output(self.LED_PIN, GPIO.LOW)
        self.light_on = False

    def change_servo_angle(self, duty_cycle):
        """
        Changes the servo motor's angle by passing him the corresponding PWM duty cycle signal
        :param duty_cycle: the length of the duty cycle
        """
        GPIO.output(self.SERVO_PIN, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        GPIO.output(self.SERVO_PIN, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def is_open(self) -> bool:
        return self.servo_status

    def light_is_on(self) -> bool:
        return self.light_on
