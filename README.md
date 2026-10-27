# Round Robin Simulator — OS_SCH_04

**Môn:** Hệ điều hành (Operating Systems) — UTH, HKI 2026–2027
**Nhóm:** OS_2627102_01 (5 thành viên)
**Đề tài:** OS_SCH_04 — *Round Robin và ảnh hưởng của time quantum*
**Hạn nộp:** Thứ Hai 09/11/2026, 23:59 — nộp 1 file `.7z` theo mẫu `ClassCode-GroupXX-ProjectCode.7z`

## Mô tả

Ứng dụng GUI (Python + Tkinter, chỉ dùng thư viện chuẩn) mô phỏng thuật toán
lập lịch CPU **Round Robin**: hàng đợi sẵn sàng (ready queue), chuyển ngữ cảnh
(context switch), và phân tích ảnh hưởng của **time quantum** tới thời gian chờ
(waiting), thời gian hoàn thành vòng (turnaround), thời gian đáp ứng (response)
và chi phí chuyển ngữ cảnh (overhead).

## Cài đặt và chạy (Windows)

1. Cài Python 3.10+ từ https://www.python.org/downloads/ (nhớ tick
   **"Add python.exe to PATH"**). Tkinter đi kèm sẵn, không cần cài thêm gì.
2. Tải/clone repo này về máy.
3. Mở thư mục `round-robin-simulator`, chạy:

```
python src/main.py
```

## Cách dùng

- Bảng bên trái là danh sách tiến trình (PID, arrival, burst) — thêm/xóa trực
  tiếp, hoặc nạp từ file CSV trong thư mục `input/`.
- Chọn **time quantum** và **thời gian chuyển ngữ cảnh** (0 = mô hình lý tưởng
  học trong lớp), bấm **RUN SIMULATION**: xem biểu đồ Gantt, bảng kết quả từng
  tiến trình và các giá trị trung bình.
- Mục **Compare quanta**: nhập nhiều quantum cách nhau dấu phẩy (ví dụ
  `1, 2, 3, 4, 5, 10`) để thấy quantum đổi thì các chỉ số đổi thế nào — phần
  phân tích chính của đề tài.
- **Save results CSV** xuất bảng kết quả ra thư mục `output/`.

Định dạng CSV đầu vào: `pid,arrival,burst` (mỗi dòng một tiến trình).
File mẫu: `input/sample_01.csv`, `input/sample_02.csv`.

## Cấu trúc thư mục

```
round-robin-simulator/
├── src/
│   ├── rr_engine.py   # Thuật toán Round Robin thuần (không phụ thuộc GUI)
│   └── main.py        # Giao diện Tkinter
├── input/             # CSV mẫu đầu vào
├── output/            # CSV kết quả xuất ra
└── docs/              # Phân công, khung báo cáo, bảng kiểm thử
```

## Quy ước làm việc nhóm (Git)

- Mỗi thành viên làm trên nhánh riêng `dev/<ten>`, xong tạo Pull Request vào
  `main`; leader review rồi merge. Lịch sử commit là một phần thầy kiểm tra.
- Commit message ngắn, rõ việc: `feat: add quantum comparison table`,
  `fix: idle segment when queue empty`, …
- Không commit file build/rác (`__pycache__` đã có trong `.gitignore`).
