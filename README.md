# WritingSkill
Một nhánh nhỏ của hệ thống, làm về rèn luyện kỹ năng viết

### Báo cáo 29/11/2025
_Vấn đề đã giải quyết từ buổi họp trước_
   + Đã bỏ các key hoặc các biến quan trọng vào file .env hay vì gán cứng vào code.
   + Sửa lại input và prompt xử lý
   + Cấu trúc lại thư mục dự án trước khi bỏ lên repo.
   + Bổ sung thêm script sh hoặc tải tự động gói thư viện và cấu hình

_Vấn đề phát sinh trong quá trình làm_
Do không có nhiều thời gian nên chưa tìm hiểu để áp dụng rag, thay vào đó dùng few-shot

_Những điều chưa hoàn thiện_
Chưa có database và thắc mắc lưu database những gì

_Định hướng phát triển_
Cải thiện AI và giao diện

### Cách chạy dự án
1. Mở git bash và clone dự án từ github:
   ```
   git clone https://github.com/OUHCMC-OUEL/WritingSkill.git
   ```
3. Chạy file run.sh để setup dự án
   ```
   cd WritingSkill
   ./run.sh
   ```
5. Đường dẫn truy cập giao diện và backend api:
   - Frontend: http://localhost:5173
   - Backend:  http://127.0.0.1:8000/

### Cấu trúc thư mục
```
WritingSkill/
├── backend/                # Mã nguồn backend (API, Django)
├── frontend/               # Mã nguồn frontend (React + Vite)
└── run.sh                  # Script tự động chạy backend + frontend
```

### Công cụ sử dụng
| Phần       | Công cụ |
|:---------- | ----:|
| front-end      | reactjs |
| back-end        | django   |
| css        | taiwind + antdesign   |
| AI       | gemini 2.5 flash  |
| deploy       | Vite   |
