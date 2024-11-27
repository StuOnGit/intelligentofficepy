import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_something(self, mock_object: Mock):
        # This is an example of test where I want to mock the GPIO.input() function
        pass

    @patch.object(GPIO, "input")
    def test_check_quadrant_occupancy_return_true(self, mock_gpio: Mock):
        io = IntelligentOffice()
        mock_gpio.side_effect = [True, False, False, False] # Used for the multiple call at the function
        result = io.check_quadrant_occupancy(io.INFRARED_PIN1)
        self.assertTrue(result)

    @patch.object(GPIO, "input")
    def test_check_quadrant_occupancy_return_true(self, mock_gpio: Mock):
        io = IntelligentOffice()
        mock_gpio.side_effect = [False, True, True, True]  # Used for the multiple call at the function
        result = io.check_quadrant_occupancy(io.INFRARED_PIN1)
        self.assertFalse(result)

    @patch.object(GPIO, "input")
    def test_check_quadrant_occupancy_raises_error(self, mock_gpio: Mock):
        io = IntelligentOffice()
        mock_gpio.side_effect = [False, True, True, True]  # Used for the multiple call at the function
        self.assertRaises(IntelligentOfficeError, io.check_quadrant_occupancy, 14) #Pin not in the board


    @patch.object(SDL_DS3231, "read_datetime")
    def test_manage_blinds_based_on_time_in_the_week_open_window(self, mock_sdl: Mock):
        io = IntelligentOffice()
        mock_sdl.return_value = datetime(2024, 1, 1, 8)
        io.manage_blinds_based_on_time()
        self.assertTrue(io.blinds_open)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_manage_blinds_based_on_time_in_the_week_close_window(self, mock_sdl: Mock):
        io = IntelligentOffice()
        mock_sdl.return_value = datetime(2024, 1, 1, 20)
        io.manage_blinds_based_on_time()
        self.assertFalse(io.blinds_open)


    @patch.object(VEML7700, "lux" , new_callable=PropertyMock)
    def test_manage_light_level_lightbulb_on(self, mock_lux: Mock):
        io = IntelligentOffice()
        mock_lux.return_value = 499
        io.manage_light_level()
        self.assertTrue(io.light_on)

    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    def test_manage_light_level_lightbulb_off(self, mock_lux: Mock):
        io = IntelligentOffice()
        mock_lux.return_value = 551
        io.manage_light_level()
        self.assertFalse(io.light_on)


    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    @patch.object(GPIO, "input")
    def test_manage_office_vacant(self, mock_gpio: Mock, mock_lux: Mock):
        mock_gpio.side_effect = [False, False, False, False]
        mock_lux.return_value = 551
        io = IntelligentOffice()
        io.manage_light_level()
        self.assertFalse(io.light_on)

    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    @patch.object(GPIO, "input")
    def test_manage_office_not_vacant(self, mock_gpio: Mock, mock_lux: Mock):
        mock_gpio.side_effect = [True, False, False, False]
        mock_lux.return_value = 499
        io = IntelligentOffice()
        io.manage_light_level()
        self.assertTrue(io.light_on)

    @patch.object(GPIO, "input")
    def test_monitor_air_quality_buzzer_on(self, mock_gpio: Mock):
        io = IntelligentOffice()
        mock_gpio.return_value = True
        io.monitor_air_quality()
        self.assertTrue(io.buzzer_on)

    @patch.object(GPIO, "input")
    def test_monitor_air_quality_buzzer_on(self, mock_gpio: Mock):
        io = IntelligentOffice()
        mock_gpio.return_value = False
        io.monitor_air_quality()
        self.assertFalse(io.buzzer_on)