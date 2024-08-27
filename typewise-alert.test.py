import unittest
from unittest.mock import patch
from io import StringIO
import typewise_alert


class TypewiseTest(unittest.TestCase):
	def test_infers_breach_as_per_limits(self):
		self.assertEqual(typewise_alert.infers_breach(20, 50, 10), 'TOO_LOW')
		self.assertEqual(typewise_alert.infers_breach(20, 50, 30), 'NORMAL')
		#self.assertEqual(typewise_alert.infers_breach(-5, 0, 35), 'TOO_LOW')
		self.assertEqual(typewise_alert.infers_breach(20,50,60), 'TOO_HIGH')

	def test_classify_temperature_breach(self):
                self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING',15),'NORMAL')
                self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 36), 'TOO_HIGH')
                self.assertEqual(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', -1), 'TOO_LOW')
                self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING',-1),'TOO_LOW')
                self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 25), 'NORMAL')
                self.assertEqual(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46), 'TOO_HIGH')
                self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 25), 'NORMAL')
                self.assertEqual(typewise_alert.classify_temperature_breach('MID_ACTIVE_COOLING',41),'TOO_HIGH')
                self.assertEqual(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', -1), 'TOO_LOW')


	@patch('sys.stdout', new_callable=StringIO)
	def test_send_to_controller(self, mock_stdout):
	  typewise_alert.send_to_controller('TOO_LOW')
	  self.assertEqual(mock_stdout.getvalue(),'65534, TOO_LOW\n')

	@patch('sys.stdout', new_callable=StringIO)
	def test_send_to_email(self, mock_stdout):
	  typewise_alert.send_to_email('TOO_HIGH')
	  expected_output = "To:a.b@cy.com\nHi, The temperature is too high\n"
	  self.assertEqual(mock_stdout.getvalue(),expected_output)

	def test_check_and_alert(self):
		with patch('__main__.send_to_controller') as mock_send_to_controller:
			typewise_alert.check_and_alert('TO_CONTROLLER', {'coolingType':'PASSIVE_COOLING'}, 25)
			mock_send_to_controller.assert_called_with('NORMAL')

		with patch('__main__.send_to_email') as mock_send_to_email:
			typewise_alert.check_and_alert('TO_EMAIL', {'coolingType':'PASSIVE_COOLING'}, -5)
			mock_send_to_controller.assert_called_with('TOO_LOW')

			typewise_alert.check_and_alert('INVALID_TARGET', {'coolingType':'PASSIVE_COOLING'}, 50)



if __name__ == '__main__':
	unittest.main()
