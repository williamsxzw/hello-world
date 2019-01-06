###############################################################################
from unittest.mock import patch
from unittest import TestCase
import unittest
from split import spliddit

class TestSplit(TestCase):
    """
    a class using unittest to test if the functions in spliddit work as expected
    """
    
    score_machine = spliddit()
        
    def test_option(self):
        # test if the option checking works as expected
        for option in ['A', 'C', 'V', 'S', 'Q']:
            expect = True
            self.assertEqual(self.score_machine.check_option(option), expect)
        for option in 'asfvKLJGH2304*&£$^815':
            expect = False
            self.assertEqual(self.score_machine.check_option(option), expect)

    def test_number(self):
        # test if the integer checking works as expected

        for num in [1, 25, 24, 32, 54100343, 44523, -1, -3134, -23]:
            expect = True
            self.assertEqual(self.score_machine.check_int(str(num)), expect)
        for num in ['0.1', '-12.3', '56.4', 'a', 'SSSD', '5.s', 'y.7', '£']:
            expect = False
            self.assertEqual(self.score_machine.check_int(str(num)), expect)

    def test_valid_zero(self):
        # test if the value range larger than 0 works as expected
        
        for num in range(0,100):
            expect = True
            self.assertEqual(self.score_machine.check_valid(num, 0), expect)
        for num in range(-100,0):
            expect = False
            self.assertEqual(self.score_machine.check_valid(num, 0), expect)
                             
    def test_valid_three(self):
        # test if the value range larger than 3 works as expected
        
        for num in range(3,100):
            expect = True
            self.assertEqual(self.score_machine.check_valid(num, 3), expect)
        for num in range(-100,3):
            expect = False
            self.assertEqual(self.score_machine.check_valid(num, 3), expect)

if __name__ == "__main__":
    unittest.main()