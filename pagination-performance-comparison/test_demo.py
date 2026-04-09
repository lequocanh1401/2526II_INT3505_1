import requests
import time

BASE_URL = 'http://127.0.0.1:5000'
PAGE_SIZE = 10

def print_result(method, page_position, exec_time, fetch_time):
    # Định dạng output dễ nhìn như một bảng
    print(f"| {method:<15} | {page_position:<25} | DB Query: {exec_time*1000:>8.2f} ms | Tổng request: {fetch_time*1000:>8.2f} ms |")

def test_pagination():
    print("=" * 86)
    print(f"{'SO SÁNH HIỆU NĂNG CÁC PHƯƠNG PHÁP PAGINATION (CƠ SỞ DỮ LIỆU 1 TRIỆU BẢN GHI)':^86}")
    print("=" * 86)
    print(f"| {'Phương pháp':<15} | {'Vị trí dữ liệu cần lấy':<25} | {'Thời gian query (DB)':<19} | {'Thời gian request':<19} |")
    print("-" * 86)
    
    # ---------------------------------------------------------
    # 1. TRANG ĐẦU TIÊN (offset = 0)
    # Ở trang đầu tiên, cả 3 phương pháp đều cho query time rất nhỏ, gần như bằng nhau.
    # ---------------------------------------------------------
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/page", params={'page': 1, 'size': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('1. Page-based', 'Trang đầu (Page 1)', res['execution_time_seconds'], fetch_time)
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/offset", params={'offset': 0, 'limit': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('2. Offset/Limit', 'Đầu dữ liệu (Offset 0)', res['execution_time_seconds'], fetch_time)
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/cursor", params={'cursor': 0, 'limit': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('3. Cursor', 'Đầu dữ liệu (Cursor 0)', res['execution_time_seconds'], fetch_time)
    print("-" * 86)

    # ---------------------------------------------------------
    # 2. VỊ TRÍ GIỮA (Giả sử bản ghi thứ 500,000)
    # Tốc độ Offset và Page-based bắt đầu chậm đáng kể. Cursor vẫn nhanh như cũ.
    # ---------------------------------------------------------
    middle_offset = 500000
    middle_page = middle_offset // PAGE_SIZE + 1
    cursor_middle = middle_offset  # Vì id trùng khớp với số thứ tự offset trong demo này
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/page", params={'page': middle_page, 'size': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('1. Page-based', f'Giữa dữ liệu (Page {middle_page})', res['execution_time_seconds'], fetch_time)
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/offset", params={'offset': middle_offset, 'limit': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('2. Offset/Limit', f'Giữa dữ liệu (Off. {middle_offset})', res['execution_time_seconds'], fetch_time)
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/cursor", params={'cursor': cursor_middle, 'limit': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('3. Cursor', f'Giữa dữ liệu (ID > {cursor_middle})', res['execution_time_seconds'], fetch_time)
    print("-" * 86)

    # ---------------------------------------------------------
    # 3. VỊ TRÍ CUỐI (Giả sử bản ghi thứ 999,990)
    # Sự khác biệt hiệu năng cực kỳ rõ ràng. Cursor nhanh gấp hàng trăm lần Offset.
    # ---------------------------------------------------------
    end_offset = 999990
    end_page = end_offset // PAGE_SIZE + 1
    cursor_end = end_offset 
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/page", params={'page': end_page, 'size': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('1. Page-based', f'Cuối dữ liệu (Page {end_page})', res['execution_time_seconds'], fetch_time)
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/offset", params={'offset': end_offset, 'limit': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('2. Offset/Limit', f'Cuối dữ liệu (Off. {end_offset})', res['execution_time_seconds'], fetch_time)
    
    start = time.time()
    res = requests.get(f"{BASE_URL}/api/cursor", params={'cursor': cursor_end, 'limit': PAGE_SIZE}).json()
    fetch_time = time.time() - start
    print_result('3. Cursor', f'Cuối dữ liệu (ID > {cursor_end})', res['execution_time_seconds'], fetch_time)
    print("=" * 86)

if __name__ == '__main__':
    print("\n[BẮT ĐẦU CHẠY DEMO]")
    try:
        # Check if server is up
        requests.get(f"{BASE_URL}/api/offset", params={'limit': 1})
    except requests.exceptions.ConnectionError:
        print("\n[LỖI] Không thể kết nối tới server!")
        print("Vui lòng chạy file `app.py` trong một terminal khác trước khi chạy file này.")
        print("Lệnh: python app.py")
        exit(1)
        
    test_pagination()
    print("\n[KẾT LUẬN]")
    print("- Offset/Limit và Page-based (bản chất giống nhau) sẽ dùng cơ chế quét qua từng row rồi bỏ lỡ (skip) dữ liệu -> Ngày càng chậm khi tra sâu.")
    print("- Cursor-based (Keyset) luôn dùng điểm đánh dấu và tìm kiếm trong Index (B-Tree Data Structure) -> Cực kỳ NHANH và ỔN ĐỊNH bất chấp độ sâu của dữ liệu.")
