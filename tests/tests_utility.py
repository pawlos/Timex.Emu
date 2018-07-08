import unittest

from utility import Bits

class tests_utils(unittest.TestCase):

	def test_bits_set_returns_true(self):
		self.assertTrue(Bits.set())

	def test_bits_reset_returns_false(self):
		self.assertFalse(Bits.reset())

	def test_bits_count_returns_8_for_value_255(self):
		self.assertEquals(8, Bits.count(255))

	def test_bits_getNthBit_returns_1_for_N_equals_2_and_value_14(self):
		self.assertEquals(1, Bits.getNthBit(14, 2))

	def test_bits_setNthBit_correctly_set_the_but(self):
		self.assertEquals(32,Bits.setNthBit(0, 5, 1))

	def test_bits_isZero_returns_true_when_value_is_zero(self):
		self.assertTrue(Bits.isZero(0))

	def test_bits_isZero_returns_false_when_value_is_non_zero(self):
		self.assertFalse(Bits.isZero(1))

	def test_bits_isEvenParity_returns_true_when_valus_has_even_number_of_1s(self):
		self.assertTrue(Bits.isEvenParity(3))