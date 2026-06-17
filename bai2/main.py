"""
main.py
-------
Điều phối trung tâm (Entry point) của hệ thống quản lý lưu trữ Rikkei Media.

Toàn bộ logic nghiệp vụ rời rạc đã được tách ra thành các package/module
độc lập (storage, analytics) theo nguyên tắc Separation of Concerns.
Chỉ import đích danh các hàm cần dùng (explicit import), không dùng `import *`.
"""

from storage.disk_manager import calculate_disk_blocks
from storage.io_helper import safe_create_dir
from analytics.time_validator import parse_and_inspect_date

# Đường dẫn gốc của kho lưu trữ media
ROOT_STORAGE_PATH = "media_vault"

# Danh sách tệp tin truyền về từ phòng hậu kỳ
raw_file_list = [
    {"filename": "pod_ep1.mp3", "size_bytes": 4500, "duration_sec": 180, "upload_at": "2026-06-10"},
    {"filename": "movie_trailer.mp4", "size_bytes": 105000, "duration_sec": 145, "upload_at": "2026-06-31"},
    {"filename": "clip_short.mp4", "size_bytes": 8200, "duration_sec": 15, "upload_at": "2026-05-15"},
]


def classify_media_type(filename):
    """
    Phân loại tệp tin theo phần mở rộng, trả về tên thư mục lưu trữ tương ứng
    (audio / video / unknown).
    """
    extension = filename.rsplit(".", 1)[-1].lower()
    if extension in ("mp3", "wav", "aac", "flac"):
        return "audio"
    if extension in ("mp4", "mov", "mkv", "avi"):
        return "video"
    return "unknown"


def process_media_file(file_info):
    """
    Xử lý toàn bộ vòng đời của một tệp tin: kiểm tra ngày tải lên, tính số
    block lưu trữ, phân loại và khởi tạo thư mục đích.

    Trả về:
        bool: True nếu tệp tin được xử lý thành công, False nếu thất bại.
    """
    filename = file_info["filename"]
    size_bytes = file_info["size_bytes"]
    upload_timestamp = file_info["upload_at"]

    print(f"\n[TỆP TIN: {filename}]")

    upload_date = parse_and_inspect_date(upload_timestamp)
    if upload_date is None:
        print(f" + Trạng thái phân loại: 🔴 THẤT BẠI (Lỗi: Định dạng ngày upload '{upload_timestamp}' không tồn tại)")
        return False

    disk_blocks = calculate_disk_blocks(size_bytes)
    media_type_folder = classify_media_type(filename)
    destination_path = f"{ROOT_STORAGE_PATH}/{media_type_folder}"
    safe_create_dir(destination_path)

    print(f" + Dung lượng thực tế: {size_bytes:,} Bytes")
    print(f" + Số khối phân vùng (4KB Block): {disk_blocks} Blocks")
    print(f" + Trạng thái phân loại: 🟢 HỢP LỆ (Lưu trữ vào thư mục '{media_type_folder}')")
    return True


def main():
    """Hàm chính: khởi tạo hạ tầng, quét toàn bộ danh sách tệp tin và in báo cáo."""
    print("======== HỆ THỐNG QUẢN LÝ LƯU TRỮ RIKKEI MEDIA ======")

    safe_create_dir(ROOT_STORAGE_PATH)
    print("[SYSTEM] Kiểm tra hạ tầng lưu trữ... Hoàn tất.")
    print("---------------------------------------------------------------------------")

    total_files = len(raw_file_list)
    success_count = 0

    for file_info in raw_file_list:
        if process_media_file(file_info):
            success_count += 1

    print("\n========================================================")
    print(f"TIẾN ĐỘ QUÉT: Hoàn thành xử lý {success_count}/{total_files} tệp tin thành công. Hệ thống ổn định.")


if __name__ == "__main__":
    main()
