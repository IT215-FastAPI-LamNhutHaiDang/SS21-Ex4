# Báo cáo Bài 4: Phân tích lỗ hổng đăng nhập

## 1. Bảng phân tích 5 vấn đề bảo mật trong code cũ

Dưới đây là 5 lỗi em tìm thấy trong đoạn code mẫu của đề bài:

| Vấn đề | Nguy cơ | Cách khắc phục |
|--------|---------|----------------|
| **1. So sánh mật khẩu trực tiếp (plaintext)** | Code cũ so sánh `data.password != user.password` nghĩa là DB đang lưu pass rõ ràng. Nếu bị hack DB là mất hết pass của user. | Dùng thư viện như `passlib` (bcrypt) để băm mật khẩu trước khi lưu và khi kiểm tra. |
| **2. Bỏ thẳng password vào payload của JWT** | Payload JWT chỉ được encode chứ không mã hóa, ai cũng có thể lên trang jwt.io dịch ra xem được. Để pass ở đây là lộ 100%. | Tuyệt đối không cho password vào trong payload khi sinh token. |
| **3. Token không có thời gian sống (expiration)** | Lúc tạo token không thấy truyền trường `exp`. Nghĩa là token này sống mãi mãi, ai trộm được là dùng luôn khỏi cần đăng nhập lại. | Thêm thời gian hết hạn (ví dụ 30 phút) vào payload. |
| **4. Secret key quá yếu ("123456")** | Secret key để ký token mà đặt là `123456` thì hacker dễ dàng đoán được và tự tạo ra token ảo với quyền Admin. | Đổi thành một chuỗi ngẫu nhiên, dài và phức tạp, tốt nhất là giấu trong biến môi trường (ví dụ file .env). |
| **5. Thông báo lỗi quá chi tiết ("Email không tồn tại")** | Báo lỗi kiểu này giúp kẻ xấu viết tool dò xem email nào đã đăng ký tài khoản trên hệ thống của mình. | Báo chung chung kiểu: "Email hoặc mật khẩu không chính xác" để hacker không biết sai ở đâu. |

## 2. Giải thích luồng xử lý sau khi em sửa (trong file main.py)

Sau khi sửa lại ở file `main.py`, luồng đăng nhập của em sẽ hoạt động an toàn hơn như sau:

- **Bước 1:** Lấy email người dùng gửi lên để tìm trong cơ sở dữ liệu.
- **Bước 2:** Dùng hàm `pwd_context.verify()` của thư viện passlib để kiểm tra mật khẩu người dùng nhập vào có khớp với mã băm (hash) lưu trong DB hay không. 
- **Bước 3:** Gộp chung lỗi. Nếu không tìm thấy user hoặc mật khẩu không đúng, em văng lỗi `HTTP 401` với dòng chữ "Email hoặc mật khẩu không chính xác". Như vậy hacker sẽ khó đoán.
- **Bước 4:** Tạo Payload cho JWT. Em chỉ lấy `id`, `email`, `role` và tạo thêm một cái thời hạn là 30 phút nữa hết hạn (trường `exp`). 
- **Bước 5:** Ký token bằng một Secret key khó đoán hơn và trả về cho Client. Client sau đó lấy cái Access Token này gài vào header để gọi các API khác.
