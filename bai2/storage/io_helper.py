"""
io_helper.py
------------
Module thuộc package `storage`, chịu trách nhiệm tương tác an toàn với
hệ thống file (tạo thư mục lưu trữ) thông qua thư viện os.
"""

import os


def safe_create_dir(path):
    """
    Khởi tạo thư mục lưu trữ một cách an toàn.

    Sử dụng os.makedirs(path, exist_ok=True) thay cho os.mkdir() vì:
        - Cho phép tạo các thư mục lồng nhau (ví dụ: media_vault/2026/video)
          trong một lần gọi duy nhất, không cần tạo từng cấp.
        - Tham số exist_ok=True giúp bỏ qua (không raise FileExistsError)
          nếu thư mục đích đã tồn tại từ trước.

    Tham số:
        path (str): Đường dẫn thư mục cần tạo.

    Trả về:
        bool: True nếu thư mục được tạo mới hoặc đã tồn tại sẵn sàng để dùng.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as error:
        print(f" [WARNING] Không thể tạo thư mục '{path}': {error}")
        return False
