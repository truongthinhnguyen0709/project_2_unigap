import json
import os
import csv

def extract_ids_from_json_files(parent_folder):
    """
    Duyệt qua tất cả các file JSON trong các thư mục con của thư mục cha,
    lấy ra ID từ mỗi file và lưu vào một file CSV duy nhất.

    Args:
        parent_folder (str): Đường dẫn đến thư mục cha.
    """

    all_ids = []
    for sub_folder in os.listdir(parent_folder):
        sub_folder_path = os.path.join(parent_folder, sub_folder)
        if os.path.isdir(sub_folder_path):
            for filename in os.listdir(sub_folder_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(sub_folder_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                for item in data:
                                    if 'id' in item:
                                        all_ids.append(item['id'])
                            elif isinstance(data, dict) and 'id' in data:
                                all_ids.append(data['id'])
                    except Exception as e:
                        print(f"Lỗi khi đọc file {file_path}: {e}")

    # Ghi tất cả các ID vào file CSV trong thư mục cha
    csv_file_path = os.path.join(parent_folder, "all_ids.csv")
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id'])  # Ghi header
            for id in all_ids:
                writer.writerow([id])
        print(f"Đã ghi tất cả các ID vào file: {csv_file_path}")
    except Exception as e:
        print(f"Lỗi khi ghi file CSV: {e}")

if __name__ == "__main__":
    parent_folder = input("Nhập đường dẫn đến thư mục cha chứa các thư mục con: ")
    extract_ids_from_json_files(parent_folder)
