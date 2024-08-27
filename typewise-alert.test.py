import unittest
import typewise_alert


class TypewiseTest(unittest.TestCase):
  def test_infers_breach_as_per_limits(self):
    self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')
    self.assertTrue(typewise_alert.infer_breach(25 0, 35) == 'NORMAL')
    self.assertTrue(typewise_alert.infer_breach(-5, 0, 35) == 'TOO_LOW')
    self.assertTrue(typewise_alert.infer_breach(40, 0, 35) == 'TOO_HIGH')

def test_classify_temperature_breach(self):
  self.assertEqual(classify_temperature_breach('PASSIVE_COOLING')


if __name__ == '__main__':
  unittest.main()
