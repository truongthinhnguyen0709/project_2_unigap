import csv
import json
import html
import time
import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor

def download_and_extract_product_info_sync(product_id, output_dir):
    """Downloads product info synchronously and saves to a JSON file."""
    api_url = f"https://api.tiki.vn/product-detail/api/v1/products/{product_id}"
    filename = os.path.join(output_dir, f"product_detail_{product_id}_missing_threaded.json")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=10)  # Thêm timeout để tránh bị treo
        response.raise_for_status()
        data = response.json()

        description_html = data.get("description", "")
        description_unescaped = html.unescape(description_html)

        product_info = {
            "id": data.get("id"),
            "name": data.get("name"),
            "url_key": data.get("url_key"),
            "price": data.get("price"),
            "description": description_unescaped,
            "image_urls": [image.get("base_url") for image in data.get("images", []) if image.get("base_url")]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(product_info, f, ensure_ascii=False, indent=4)
        print(f"ID: {product_id}, Status: {response.status_code} (Missing Threaded)")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Lỗi HTTP cho ID {product_id} (Missing Threaded): {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Lỗi JSON cho ID {product_id} (Missing Threaded): {e}")
        return False
    except IOError as e:
        print(f"Lỗi IO cho ID {product_id} (Missing Threaded): {e}")
        return False
    except Exception as e:
        print(f"Lỗi không xác định cho ID {product_id} (Missing Threaded): {e}")
        return False

def process_missing_product_ids_parallel(missing_product_ids, output_dir, max_workers=5):
    """Processes a list of missing product IDs in parallel using threads."""
    successful_downloads = 0
    failed_downloads = 0
    total_missing = len(missing_product_ids)
    print(f"Bắt đầu xử lý {total_missing} ID bị thiếu (threaded).")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Lưu kết quả vào thư mục: {output_dir}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_and_extract_product_info_sync, pid, output_dir) for pid in missing_product_ids]
        for future in futures:
            if future.result():
                successful_downloads += 1
            else:
                failed_downloads += 1
    print(f"  Đã tải thành công (missing threaded): {successful_downloads}/{total_missing}")
    print(f"  Lỗi (missing threaded): {failed_downloads}/{total_missing}")
    print("Hoàn tất xử lý các ID bị thiếu (threaded).")

def main_missing():
    missing_ids_file = "cac_id_bi_thieu.csv"  # Tên file chứa 1083 ID bị thiếu, mỗi ID trên một dòng
    output_directory = "tiki_miss"
    max_workers = 10

    if not os.path.exists(missing_ids_file):
        print(f"Không tìm thấy file chứa ID bị thiếu: {missing_ids_file}")
        return

    try:
        with open(missing_ids_file, 'r') as f:
            missing_product_ids = [line.strip() for line in f if line.strip()]
        num_missing = len(missing_product_ids)
        print(f"Đọc thành công {num_missing} ID bị thiếu từ file: {missing_ids_file}")
        process_missing_product_ids_parallel(missing_product_ids, output_directory, max_workers)

    except FileNotFoundError:
        print(f"Không tìm thấy file: {missing_ids_file}")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi đọc file ID bị thiếu: {e}")

if __name__ == "__main__":
    main_missing()
