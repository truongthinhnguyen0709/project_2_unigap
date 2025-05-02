# project_2_unigap
* Bước 1: Tách file csv tổng chứa 200.000 product id ra thành các file csv nhỏ hơn chứa 1000 product id code thực hiện được lưu trong tach_file_csv

#Bước 2: Sử dụng threading để gửi request đến api tiki 
* Sử dụng code trong file "project_test_threading"
* Tải về được tổng cộng: 198.917 / 200.000
* Lỗi tổng cộng: 1083 sản phẩm

#Bước 3: Lưu các id thiếu và bị lỗi sang 1 file mới và tải lại
* Tải về thành công thêm 18 id
* Lỗi 404 với 1065 sản phẩm
* Tổng cộng tải về thành công 198.935 sản phẩm



