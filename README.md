# Apimid
## Tổng quan
>Giao diện người dùng được xây dựng trên ứng dụng Android với các dữ liệu được truy xuất và xử lý thông qua các máy chủ (Server) được triển khai sử dụng Flask Framework.
>Ngoài ra Đánh giá chương trình trên bài toán nhận dạng vùng văn bản trong các hình ảnh tài liệu có nềnphức tạpcó một giao diện quản lý trên Web được thiết lập dựa trên Spring Framework. Kiến trúc tổngquát được minh họa như trong hình:



![alt text](https://gitlab.com/namhcn/apimid/blob/master/static/images/AppArch.png)

## Triển khai máy chủ cho ứng dụng Android
Phía máy chủ gồm 3 thành phần chính:
- [x] Sử dụng Nginx là một máy chủ proxy ngược mã nguồn mở, tập trung vào việc phục vụ số lượng kết nối đồng thời lớn (high concurrency), hiệu suất cao và sử dụng bộ nhớ thấp.
- [x] Một máy chủ trung gian kết nối trực tiếp với Nginx (minh họa trong hình \ref{fig:Kientruc}) để nhận yêu cầu và phân loại yêu cầu để  chuyển tiếp sang máy chủ khác hoặc truy xuất cơ sở dữ liệu để đáp ứng yêu cầu đó.
- [x] Máy chủ nhận yêu cầu nhận dạng vùng văn bản từ máy máy chủ trung gian. Máy chủ này đã được triển khai và đang chạy mô hình đã được đào tạo và chỉ chờ nhận yêu cầu nhận dạng và phản hồi cho máy chủ trung gian.

## Cơ sở dữ liệu
Ứng dụng web truy xuất dữ liệu trực tiếp từ cơ sở dữ liệu MySQL từ đó cho phép người quản lý có thể thực hiện chức năng như sau:

- [x] Theo dõi, trực quan hóa cơ sở dữ liệu và có thể thực hiện trực tiếp tác vụ xóa. 
- [x] Thông kê số lượng yêu cầu thực hiện chức năng nhận dạng vùng văn bản của người dùng trên hệ thông Android theo từng ngày.

## Chi tiết ApiMid
ApiMid là hệ thống viết bằng framework Flask nằm giữa Ngix, Myslq, Tensorflow Server nhằm cung cấp các API cho ứng dụng Android: 

- [x] Post Request cho việc nhận diện vùng văn bản.
- [x] Get Request cho việc lấy ảnh và truy vấn lịch sử.
- [x] Put Request cho việc chỉnh sửa nội dung vùng văn bản.
- [x] Delete Request cho việc xóa ảnh đã được lưu trữ.
## Đóng góp
@NamNguyenThanh
