import unittest

from utility import Bits, IndexToReg

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

	def test_bits_limitTo8Bits_correctly_limits_value_to_8_bits(self):
		value = 0b1101010010
		self.assertEquals(0b1010010, Bits.limitTo8Bits(value))

	def test_bits_isNegative_returns_true_if_value_is_over_80h(self):
		self.assertTrue(Bits.isNegative(0x81))

	def test_bits_isNegative_returns_false_if_value_is_below_80h(self):
		self.assertFalse(Bits.isNegative(0x20))

	def test_bits_isNegative_returns_true_for_16bit_if_value_is_over_8000h(self):
		self.assertTrue(Bits.isNegative(0x8000, bits=16))

	def test_bits_isNegative_returns_false_for_16bit_if_value_is_below_8000h(self):
		self.assertFalse(Bits.isNegative(0x2000, bits=16))

	def test_IndexToReg_translate8Bit_returns_B_for_0(self):
		self.assertEquals("B", IndexToReg.translate8Bit(0))

	def test_IndexToReg_trasnalte8Bit_returns_C_for_1(self):
		self.assertEquals("C", IndexToReg.translate8Bit(1))