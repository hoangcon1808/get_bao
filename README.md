Đây là bản **README.md** chuyên nghiệp và đầy đủ để bạn đưa lên GitHub cùng với dự án của mình. Một file README tốt không chỉ giúp bạn quản lý dự án hiệu quả mà còn ghi điểm lớn nếu bạn dùng nó để làm Portfolio.
# 📰 News Hub - Vietnamese Multi-Source News Aggregator
**News Hub** là một ứng dụng web nhẹ, hiện đại được xây dựng bằng **Python (Flask)**, cho phép tự động lấy tin tức mới nhất từ 6 tờ báo hàng đầu Việt Nam. Ứng dụng được tối ưu hóa để triển khai trên nền tảng **Vercel** dưới dạng Serverless Functions.
## ✨ Tính năng nổi bật
 * **Đa nguồn tin:** Tự động cào dữ liệu từ 6 báo lớn: VNExpress, Tuổi Trẻ, Thanh Niên, Dân Trí, VietnamNet, và Znews.
 * **Hiển thị hiện đại:** Giao diện tối (Dark Mode) với thiết kế thanh cuộn ngang (Horizontal Scroll) tương tự Netflix, giúp tiết kiệm diện tích và dễ theo dõi.
 * **Cào dữ liệu song song (Parallel Scraping):** Sử dụng ThreadPoolExecutor để lấy dữ liệu từ 6 trang cùng lúc, đảm bảo tốc độ phản hồi cực nhanh (< 3 giây) và tránh bị timeout trên Vercel.
 * **Cơ chế chống Block:**
   * Xoay vòng ngẫu nhiên **User-Agent**.
   * Giả lập **Referer** từ Google.
   * Xử lý ảnh **Lazy Load** (lấy đúng link ảnh thực).
 * **Tương thích thiết bị:** Hỗ trợ cuộn ngang bằng con lăn chuột trên máy tính và vuốt chạm trên điện thoại.
## 🛠 Công nghệ sử dụng
 * **Backend:** Python 3.x, Flask.
 * **Scraping:** BeautifulSoup4, Requests.
 * **Frontend:** HTML5, CSS3 (Flexbox), JavaScript (Vanilla).
 * **Deployment:** Vercel (Serverless Functions).
## 📂 Cấu trúc thư mục
```text
news-app/
├── api/
│   └── index.py        # Mã nguồn chính xử lý Flask & Scraping
├── requirements.txt    # Danh sách thư viện cần thiết
├── vercel.json         # File cấu hình triển khai lên Vercel
└── README.md           # Hướng dẫn này

```
## 🚀 Hướng dẫn cài đặt và chạy cục bộ
 1. **Clone repository:**
   ```bash
   git clone https://github.com/username/news-hub.git
   cd news-hub
   
   ```
 2. **Cài đặt thư viện:**
```bash
   pip install -r requirements.txt

```
 3. **Chạy ứng dụng:**
   ```bash
   python api/index.py
   
   ```
   Sau đó truy cập [http://127.0.0.1:5000](http://127.0.0.1:5000) trên trình duyệt.
## ☁️ Triển khai lên Vercel
 1. Đẩy mã nguồn lên một repository trên **GitHub**.
 2. Truy cập Vercel.com và tạo dự án mới từ GitHub repo đó.
 3. Vercel sẽ tự động nhận diện cấu hình trong vercel.json và triển khai.
 4. **Xong!** Bạn sẽ nhận được một domain .vercel.app để truy cập từ bất cứ đâu.
## ⚠️ Lưu ý quan trọng (Disclaimer)
 * **Mục đích giáo dục:** Dự án này được tạo ra nhằm mục đích học tập kỹ thuật Scraping và triển khai ứng dụng Python.
 * **Bản quyền:** Ứng dụng không lưu trữ dữ liệu. Tất cả tiêu đề và hình ảnh đều thuộc bản quyền của các tờ báo tương ứng. Vui lòng tôn trọng chính sách của các báo khi sử dụng dữ liệu.
 * **Bảo trì:** Các báo có thể thay đổi cấu trúc HTML bất cứ lúc nào. Nếu dữ liệu không hiển thị, bạn cần cập nhật lại các selector (CSS Class) trong file api/index.py.
## 🤝 Đóng góp
Mọi ý kiến đóng góp hoặc báo lỗi, vui lòng mở **Issue** hoặc gửi **Pull Request**. Rất vui khi nhận được sự hỗ trợ từ cộng đồng!
*Cảm ơn bạn đã ghé thăm dự án! Nếu thấy hữu ích, đừng quên tặng mình 1 ⭐ trên GitHub nhé.*
```

```
