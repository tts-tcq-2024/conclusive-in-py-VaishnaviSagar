import unittest
from unittest.mock import patch
from io import StringIO

class TestTemperatureBreachDetection(unittest.TestCase):
    def test_infer_breach(self):
        self.assertEqual(infer_breach(25, 0, 35), 'NORMAL')
        self.assertEqual(infer_breach(-5, 0, 35), 'TOO_LOW')
        self.assertEqual(infer_breach(40, 0, 35), 'TOO_HIGH')

    def test_classify_temperature_breach(self):
        self.assertEqual(classify_temperature_breach('PASSIVE_COOLING', 25), 'NORMAL')
        self.assertEqual(classify_temperature_breach('HI_ACTIVE_COOLING', -5), 'TOO_LOW')
        self.assertEqual(classify_temperature_breach('MED_ACTIVE_COOLING', 50), 'TOO_HIGH')
        self.assertEqual(classify_temperature_breach('INVALID_TYPE', 25), 'TOO_LOW')

    @patch('sys.stdout', new_callable=StringIO)
    def test_send_to_controller(self, mock_stdout):
        send_to_controller('TOO_LOW')
        self.assertEqual(mock_stdout.getvalue(), '65534, TOO_LOW\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_send_to_email(self, mock_stdout):
        send_to_email('TOO_HIGH')
        expected_output = "To:a.b@c.com\nHi, The temperature is too high\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_check_and_alert(self):
        battery_char = {'coolingType': 'PASSIVE_COOLING'}
        with patch('__main__.send_to_controller') as mock_send_to_controller:
            check_and_alert('TO_CONTROLLER', battery_char, 25)
            mock_send_to_controller.assert_called_with('NORMAL')

        with patch('__main__.send_to_email') as mock_send_to_email:
            check_and_alert('TO_EMAIL', battery_char, -5)
            mock_send_to_email.assert_called_with('TOO_LOW')

        check_and_alert('INVALID_TARGET', battery_char, 50)

if __name__ == '__main__':
    unittest.main()
