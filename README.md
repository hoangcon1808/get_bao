Đây là bản **README.md** được thiết kế riêng cho mô hình **GitHub Actions + GitHub Pages**. Bản này tập trung vào việc hướng dẫn cách vận hành hệ thống tự động cào dữ liệu và cập nhật web mà không cần server.
# 📰 News Hub (GitHub Edition)
**News Hub** là một trang web tổng hợp tin tức tự động từ 6 đầu báo lớn tại Việt Nam. Dự án sử dụng cơ chế **Static Site Generation (SSG)** kết hợp với **GitHub Actions** để tự động cập nhật dữ liệu mỗi 15 phút.
## ⚙️ Cơ chế hoạt động
Hệ thống hoạt động theo mô hình tự động hóa hoàn toàn:
 1. **Scraper (GitHub Actions):** Cứ mỗi 15 phút, một máy ảo Ubuntu sẽ tự động khởi động, chạy script Python (scraper.py).
 2. **Data Storage:** Kết quả cào được lưu vào file data.json và được bot tự động commit/push ngược lại vào Repository.
 3. **Frontend (GitHub Pages):** Khi người dùng truy cập, trình duyệt sẽ tải file index.html và fetch dữ liệu từ data.json để hiển thị.
## 📂 Cấu trúc dự án
```text
.
├── .github/workflows/
│   └── scrape.yml      # Lịch trình chạy tự động (Cron job)
├── scraper.py          # Script cào dữ liệu (Python + BeautifulSoup4)
├── index.html          # Giao diện hiển thị (HTML/JS)
├── data.json           # File chứa dữ liệu tin tức (Tự động cập nhật)
└── requirements.txt    # Thư viện Python cần thiết

```
## 🚀 Hướng dẫn thiết lập (Setup)
Để tự tạo một bản News Hub cho riêng mình, hãy thực hiện các bước sau:
### 1. Fork hoặc Tạo mới Repository
 * Đưa toàn bộ code lên một Repo trên GitHub của bạn.
### 2. Cấp quyền cho GitHub Actions (Quan trọng)
Để script có thể tự động lưu file data.json, bạn cần cấp quyền ghi:
 * Vào **Settings** -> **Actions** -> **General**.
 * Cuộn xuống mục **Workflow permissions**.
 * Chọn **Read and write permissions**.
 * Bấm **Save**.
### 3. Kích hoạt GitHub Pages
 * Vào **Settings** -> **Pages**.
 * Tại mục **Build and deployment**, chọn Branch là main và thư mục là /(root).
 * Bấm **Save**. Sau vài phút, bạn sẽ nhận được đường link trang web của mình.
### 4. Chạy thử lần đầu
 * Vào tab **Actions** trên GitHub.
 * Chọn workflow **Auto Scrape News**.
 * Bấm **Run workflow** -> **Run workflow**.
 * Đợi khoảng 1 phút, nếu hiện dấu tích xanh ✅ nghĩa là dữ liệu đã được cào thành công.
## 🛠 Công nghệ sử dụng
 * **Ngôn ngữ:** Python (Scraping), JavaScript (Rendering).
 * **Thư viện:** BeautifulSoup4, Requests.
 * **Hệ thống:** GitHub Actions, GitHub Pages.
## ⚠️ Lưu ý
 * **Độ trễ:** GitHub Actions đôi khi có thể chạy trễ hơn lịch trình cron khoảng vài phút tùy thuộc vào hàng đợi của hệ thống GitHub.
 * **Bản quyền:** Dự án này chỉ phục vụ mục đích học tập kỹ thuật. Vui lòng không sử dụng dữ liệu cào được cho các mục đích thương mại vi phạm bản quyền báo chí.
## 🤝 Đóng góp
Nếu bạn muốn bổ sung thêm các nguồn báo khác, hãy chỉnh sửa biến SOURCES trong file scraper.py và gửi một bản Pull Request!
*Dự án được vận hành hoàn toàn miễn phí trên hạ tầng của GitHub.*
