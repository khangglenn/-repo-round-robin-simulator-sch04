# PHÂN CÔNG CÔNG VIỆC — Nhóm OS_2627102_01

Đề tài OS_SCH_04: Round Robin và ảnh hưởng của time quantum.
Hạn nộp: Thứ Hai 09/11/2026 23:59 (nộp sớm mục tiêu: 08/11).

| # | Thành viên | Phần việc chính | Sản phẩm bàn giao | Phần quay video |
|---|------------|-----------------|-------------------|-----------------|
| 1 | Kim Văn Bảo Khang (nhóm trưởng) | Quản lý repo GitHub, review/merge PR, tích hợp các phần, README, đóng gói file .7z đúng mẫu tên, nộp bài | Repo hoàn chỉnh, file nộp `ClassCode-GroupXX-ProjectCode.7z` | Mở đầu: giới thiệu đề tài, nhóm, phân công |
| 2 | Nguyễn Trần Tiến | Thuật toán lõi `src/rr_engine.py`: ready queue, context switch, tính waiting/turnaround/response; viết test kiểm chứng thuật toán | Engine chạy đúng, bộ test case | Trình bày thuật toán Round Robin và cách cài đặt |
| 3 | Huỳnh Minh Triết | Giao diện `src/main.py`: bảng nhập tiến trình, nạp CSV, điều khiển quantum; kiểm tra chạy trên Windows | GUI hoàn chỉnh, chạy được trên Windows | Demo thao tác trên giao diện |
| 4 | Nguyễn Long Vũ | Trực quan hóa và phân tích: biểu đồ Gantt, bảng/biểu đồ so sánh nhiều quantum (response time ↔ số lần context switch ↔ overhead) | Hình/bảng phân tích cho báo cáo + slide | Trình bày kết quả phân tích ảnh hưởng của quantum |
| 5 | Lê Hiền Hải Đăng | Báo cáo Word theo khung 7 mục + trả lời 6 câu hỏi bắt buộc; bảng kiểm thử; PowerPoint; kịch bản video | Báo cáo, bảng kiểm thử, file slide | Tổng kết: khó khăn, bài học, việc chưa làm |

## Quy định chung

- Mỗi người làm trên nhánh `dev/<ten-khong-dau>` trong repo, commit bằng
  đúng tên mình — thầy kiểm tra lịch sử GitHub để chấm đóng góp.
- Xong phần thì tạo Pull Request, nhóm trưởng merge. Không push thẳng lên `main`.
- Video báo cáo: mỗi thành viên tự quay phần mình, **phải hiện mặt**, nói rõ
  phần việc đã làm; nhóm trưởng ghép và đăng Drive/YouTube (public/unlisted
  có link), link để trong báo cáo.

## Mốc tiến độ đề xuất

- **Đến 31/10:** engine + GUI chạy hoàn chỉnh, test xong (bảng kiểm thử có kết quả).
- **Đến 04/11:** xong phân tích quantum, hình/biểu đồ cho báo cáo.
- **Đến 07/11:** báo cáo Word + PowerPoint xong; quay và ghép video.
- **08/11:** đóng gói .7z, nộp lần 1. 09/11 chỉ để dự phòng sửa/nộp lại.
