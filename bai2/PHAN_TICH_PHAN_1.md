# PHẦN 1: PHÂN TÍCH VÀ THIẾT KẾ KIẾN TRÚC (30 Điểm)

## Câu 1: Tác hại của `from datetime import *`

`from datetime import *` đưa TOÀN BỘ các tên (class, hằng số) được khai báo
trong `__all__` của module `datetime` trực tiếp vào không gian tên (namespace)
hiện tại. Tác hại chính:

- **Ô nhiễm namespace (Namespace pollution):** không thể biết chắc một tên
  (ví dụ `date`, `time`, `timezone`) đến từ đâu khi đọc lại code, gây khó khăn
  cho việc bảo trì và debug.
- **Ghi đè biến đã tồn tại (Name collision):** nếu trong code đã có biến cùng
  tên với một thành phần của `datetime`, biến đó sẽ bị ghi đè (hoặc ghi đè
  ngược lại tùy thứ tự khai báo), dẫn đến lỗi logic âm thầm (silent bug) rất
  khó phát hiện vì chương trình không báo lỗi cú pháp.
- **Không tương thích công cụ phân tích tĩnh:** các IDE/linter không thể xác
  định chính xác nguồn gốc của tên, làm mất khả năng gợi ý và cảnh báo sớm.

**Trường hợp cụ thể `time = 120`:**

Module `datetime` có một class tên là `time` (đại diện cho thời điểm trong
ngày, ví dụ `datetime.time(14, 30)`) và class này **có nằm trong `__all__`**
của module. Do đó khi thực hiện:

```python
time = 120
from datetime import *   # thực thi SAU khi time = 120 đã tồn tại
print(time)               # -> <class 'datetime.time'>, KHÔNG còn là 120
```

Biến `time = 120` sẽ bị **ghi đè hoàn toàn** bởi class `datetime.time`. Toàn
bộ logic phía sau từng tham chiếu đến biến `time` với kỳ vọng đó là số 120
(ví dụ thực hiện `time + 10`) sẽ ném ra lỗi:

```
TypeError: unsupported operand type(s) for +: 'type' and 'int'
```

Đây chính là một dạng lỗi "âm thầm" cực nguy hiểm: không sai cú pháp, không
báo lỗi ngay tại dòng import, mà chỉ phát nổ (crash) ở một vị trí khác hoàn
toàn trong code — rất khó truy ngược nguyên nhân nếu không biết về cơ chế
`import *`.

## Câu 2: Hàm tạo thư mục lồng nhau an toàn

Thay vì `os.mkdir()` (chỉ tạo được 1 cấp, và crash với `FileExistsError` nếu
thư mục đã tồn tại), nên dùng:

```python
os.makedirs(path, exist_ok=True)
```

- `os.makedirs()`: cho phép tạo nhiều cấp thư mục lồng nhau trong một lần gọi
  duy nhất (ví dụ `media_vault/2026/video` được tạo cả 3 cấp nếu chưa có).
- `exist_ok=True`: bỏ qua, không ném lỗi nếu thư mục đích (hoặc một phần
  đường dẫn) đã tồn tại sẵn — giải quyết triệt để lỗi `FileExistsError` của
  code gốc.

## Câu 3: Cấu trúc cây thư mục (Package/Module)

```
rikkei_media/
│
├── main.py                    # Điều phối trung tâm, entry point của hệ thống
│
├── storage/                   # Package xử lý lưu trữ vật lý
│   ├── __init__.py
│   ├── disk_manager.py        # Tính toán block đĩa (dùng math)
│   └── io_helper.py           # Tạo thư mục an toàn (dùng os)
│
└── analytics/                 # Package phân tích nghiệp vụ
    ├── __init__.py
    └── time_validator.py      # Kiểm tra & bẫy lỗi ngày tháng (dùng datetime)
```

**Lý do tổ chức:**

- Mỗi package gom nhóm các module có cùng mối quan tâm (Separation of
  Concerns): `storage` lo việc vật lý (đĩa cứng, thư mục), `analytics` lo
  việc phân tích dữ liệu thời gian.
- `__init__.py` đánh dấu thư mục là một package Python hợp lệ, có thể mở
  rộng để export các hàm public ra ngoài nếu cần.
- `main.py` chỉ đóng vai trò điều phối (orchestration), không chứa logic
  nghiệp vụ chi tiết — dễ đọc, dễ kiểm thử (unit test) từng module độc lập.
