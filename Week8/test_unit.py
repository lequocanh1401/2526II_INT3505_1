# test_unit.py
import unittest
from app import calculate_total

class TestBusinessLogic(unittest.TestCase):
    
    def test_calculate_total_normal(self):
        # Kỳ vọng: 10 * 2 phải bằng 20
        result = calculate_total(10, 2)
        self.assertEqual(result, 20)
        
    def test_calculate_total_negative(self):
        # Kỳ vọng: nhập số âm thì code phải tự trả về 0 để khỏi lỗi hệ thống
        result = calculate_total(-5, 2)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()