# BẢNG KIỂM THỬ — Round Robin Simulator

| # | Trường hợp | Đầu vào | Kỳ vọng | Kết quả thực tế | Đạt |
|---|-----------|---------|---------|-----------------|-----|
| 1 | Ví dụ tính tay cơ bản | P1(0,5), P2(1,3), P3(2,1); quantum 2; CS time 0 | Gantt: P1 0–2, P2 2–4, P3 4–5, P1 5–7, P2 7–8, P1 8–9; waiting P1=4, P2=4, P3=2; 5 lần context switch | Khớp hoàn toàn (kiểm chứng 24/10/2026) | ✔ |
| 2 | Có chi phí chuyển ngữ cảnh | Cùng bộ trên; CS time 1 | Overhead = 5; tổng thời gian = 14 | Khớp (14, overhead 5) | ✔ |
| 3 | CPU nhàn rỗi đầu phiên | P1(3,2); quantum 1 | Có đoạn IDLE 0–3; waiting = 0; hoàn thành lúc 5 | Khớp | ✔ |
| 4 | Quantum lớn ≥ burst lớn nhất | sample_01; quantum 10 | Hành vi tương đương FCFS; số context switch tối thiểu | q=5 và q=10 cho cùng kết quả (avg waiting 5.0) | ✔ |
| 5 | So sánh nhiều quantum | sample_01; q = 1, 2, 3, 4, 5, 10 | Bảng so sánh đầy đủ; quantum nhỏ → response tốt hơn, nhiều context switch hơn | Đúng xu hướng (q=1: response 1.2, 14 switches; q=10: response 5.0, 4 switches) | ✔ |
| 6 | Nạp/xuất CSV | input/sample_02.csv | Nạp đúng 6 tiến trình; xuất results CSV mở đọc được | Chưa kiểm trên GUI Windows | ☐ |
| 7 | Chạy trên Windows | Máy Windows, Python 3.10+ | Mở GUI không lỗi, chạy mô phỏng được | Chờ kiểm thử trên máy Windows của nhóm | ☐ |

Ghi chú: các dòng 1–5 đã kiểm chứng bằng script tự động trên engine
(24/10/2026). Dòng 6–7 do Huỳnh Minh Triết (GUI) và nhóm trưởng xác nhận
trước khi nộp, chụp màn hình đưa vào báo cáo.
