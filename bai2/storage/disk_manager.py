"""
disk_manager.py
----------------
Module thuộc package `storage`, chịu trách nhiệm tính toán dung lượng
lưu trữ tối ưu theo khối dữ liệu (block) của ổ đĩa.
"""

import math


def calculate_disk_blocks(size_bytes, block_size=4096):
    """
    Tính số khối (block) ổ đĩa cần thiết để lưu trữ một tệp tin.

    Sử dụng math.ceil() để LÀM TRÒN LÊN, vì một block đã bị chiếm dụng
    một phần thì vẫn phải tính trọn 1 block (không thể dùng block lẻ).

    Tham số:
        size_bytes (int | float): Dung lượng thực tế của tệp tin (Bytes).
        block_size (int): Kích thước 1 block phân vùng ổ đĩa (mặc định 4096 = 4KB).

    Trả về:
        int: Số block cần cấp phát.
    """
    if size_bytes < 0:
        raise ValueError("Dung lượng tệp tin không thể là số âm.")

    return math.ceil(size_bytes / block_size)
