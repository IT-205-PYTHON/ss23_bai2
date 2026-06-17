"""
time_validator.py
------------------
Module thuộc package `analytics`, chịu trách nhiệm phân tích và kiểm tra
tính hợp lệ của mốc thời gian tải lên (Upload Timestamp).

Lưu ý: chỉ import đích danh class `datetime` từ thư viện chuẩn `datetime`,
KHÔNG dùng `from datetime import *` để tránh ô nhiễm không gian tên (namespace
pollution) và xung đột với các biến nội bộ khác trong dự án.
"""

from datetime import datetime


def parse_and_inspect_date(date_str, date_format="%Y-%m-%d"):
    """
    Phân tích chuỗi ngày tháng và kiểm tra tính hợp lệ.

    Sử dụng try-except để bẫy lỗi ValueError khi chuỗi ngày tháng không
    tồn tại trên thực tế (ví dụ: "2026-06-31", vì tháng 6 chỉ có 30 ngày),
    thay vì để chương trình bị crash.

    Tham số:
        date_str (str): Chuỗi ngày tháng cần kiểm tra.
        date_format (str): Định dạng mong đợi (mặc định "%Y-%m-%d").

    Trả về:
        datetime | None: Đối tượng datetime nếu hợp lệ, None nếu không hợp lệ
        (kèm theo một dòng cảnh báo được in ra console).
    """
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        print(f" [WARNING] Định dạng ngày upload '{date_str}' không tồn tại")
        return None
