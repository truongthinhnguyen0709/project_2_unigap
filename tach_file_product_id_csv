import csv
import os

def split_csv(input_filepath, output_dir="split_csv_files", lines_per_file=1000, id_column="product_id"):
    """
    Splits a large CSV file into smaller CSV files with a specified number of lines.

    Args:
        input_filepath (str): Path to the input CSV file.
        output_dir (str): Directory to save the split CSV files.
        lines_per_file (int): Number of lines (excluding header) per output file.
        id_column (str): Name of the column containing the product ID.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_number = 1
    row_count = 0
    output_file = None
    writer = None
    header = None

    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read the header row

            for row in reader:
                if row_count % lines_per_file == 0:
                    if output_file:
                        output_file.close()
                    output_filename = os.path.join(output_dir, f"products_{file_number}.csv")
                    output_file = open(output_filename, 'w', newline='', encoding='utf-8')
                    writer = csv.writer(output_file)
                    writer.writerow(header)  # Write the header to the new file
                    file_number += 1
                    row_count = 0  # Reset row count for the new file

                writer.writerow(row)
                row_count += 1

            if output_file:
                output_file.close()

        print(f"Đã cắt file '{input_filepath}' thành công thành {file_number - 1} file trong thư mục '{output_dir}'.")

    except FileNotFoundError:
        print(f"Không tìm thấy file: '{input_filepath}'")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    input_csv_file = "product_id_tiki.csv"  # Thay bằng đường dẫn đến file CSV 200 ngàn ID của bạn
    output_directory = "split_product_id_files"  # Tên thư mục để lưu các file đã cắt
    lines_per_file = 1000
    product_id_column_name = "product_id"  # Đảm bảo tên cột ID chính xác

    split_csv(input_csv_file, output_directory, lines_per_file, product_id_column_name)
