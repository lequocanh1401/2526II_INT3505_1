# test_integration.py
import unittest
import json
from app import app

class TestAPIEndpoint(unittest.TestCase):
    
    def setUp(self):
        # Tạo một 'trình duyệt ảo' để gọi API mà không cần bật server
        self.client = app.test_client()

    def test_api_success(self):
        # 1. Gửi giả lập một POST Request có chứa file JSON
        payload = {'price': 50, 'quantity': 2}
        response = self.client.post('/api/calculate', 
                                    data=json.dumps(payload), 
                                    content_type='application/json')
        
        # 2. Kiểm tra mã trạng thái phải là 200 OK
        self.assertEqual(response.status_code, 200)
        
        # 3. Kiểm tra xem file JSON trả về có ra số 100 không
        data = json.loads(response.data)
        self.assertEqual(data['total'], 100)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()