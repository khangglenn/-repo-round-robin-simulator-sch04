# HƯỚNG DẪN DÙNG KHUNG — đọc 5 phút là làm được

## Khung này là cái gì

App mô phỏng thuật toán Round Robin: nhập danh sách tiến trình, chọn
quantum, bấm RUN là ra biểu đồ Gantt với bảng thời gian chờ, thời gian
đáp ứng, thời gian hoàn thành. Đề tài của nhóm là xem quantum đổi thì
các con số này đổi ra sao.

## Chạy thử trong 1 phút

1. Cài Python 3.10 trở lên, nhớ tick "Add python.exe to PATH".
2. Mở terminal trong thư mục `round-robin-simulator`, chạy:

```text
python src/main.py
```

3. App mở sẵn 2 tiến trình mặc định. Thuật toán đang chờ Tiến viết nên
   bấm RUN sẽ hiện thông báo chờ, sau khi Tiến viết xong thì bấm RUN là
   thấy Gantt.
Không cần cài thêm thư viện gì.

## Ai mở file nào — chỉ sửa phần mình, đừng đụng phần người khác

| Người | Mở file này | Đừng đụng vào | Việc đầu tiên |
|---|---|---|---|
| Khang (nhóm trưởng) | Báo cáo Word, PowerPoint, video, file .7z | Code của 4 người (chỉ gộp khi review, không sửa bừa) | Viết báo cáo, slide, dựng video, đóng gói, nộp bài |
| Tiến | `src/rr_engine.py` | `src/main.py` | Tự viết hàm `simulate_round_robin` với `compare_quanta` theo 6 bước trong mục thuật toán, tự thêm file CSV mẫu vào `input/`, rồi viết test đối chiếu |
| Triết | `src/main.py` | `src/rr_engine.py` | Chạy GUI trên Windows, chụp màn hình đưa vào báo cáo |
| Long Vũ | File `src/charts.py` mới (tự viết) | Logic chạy trong `simulate_round_robin` | Viết code vẽ biểu đồ so sánh quantum, xuất hình cho báo cáo |
| Hải Đăng | File `src/export.py` mới (tự viết) | Code engine với giao diện của Tiến với Triết | Viết code xuất bảng kết quả với trace chi tiết |

## Thuật toán nói bằng tiếng người

Round Robin nghĩa là xếp hàng: mỗi tiến trình được chạy một lát bằng
quantum rồi về cuối hàng, cứ thế cho tới khi xong hết.

1. Xếp tiến trình theo thời gian đến, đến cùng lúc thì theo tên.
2. Lấy tiến trình đầu hàng ra, cho chạy tối đa một quantum. Chạy hết
   phần còn lại thì xong, khỏi xếp lại.
3. Trong lúc chạy, tiến trình nào đến mới thì xếp vào cuối hàng.
4. Hết một lát mà chưa chạy xong thì xếp lại cuối hàng.
5. Đổi sang tiến trình khác thì đếm 1 lần context switch. Nếu có chi
   phí chuyển ngữ cảnh thì cộng thêm đoạn đó vào thời gian.
6. Hàng rỗng mà vẫn còn tiến trình chưa đến thì CPU ngồi chơi (IDLE)
   tới lúc tiến trình tiếp theo đến.

## Ví dụ chạy tay — kết quả đúng mà code của Tiến phải cho ra

P1 (đến 0, chạy 5), P2 (đến 1, chạy 3), P3 (đến 2, chạy 1), quantum 2,
không tính chi phí chuyển ngữ cảnh:

- 0–2: P1 chạy, còn 3 → hàng [P2, P3, P1]
- 2–4: P2 chạy, còn 1 → hàng [P3, P1, P2]
- 4–5: P3 chạy xong → hàng [P1, P2]
- 5–7: P1 chạy, còn 1 → hàng [P2, P1]
- 7–8: P2 chạy xong → hàng [P1]
- 8–9: P1 chạy xong.

Kết quả: P1 chờ 4, P2 chờ 4, P3 chờ 2; đổi người 5 lần.
Sau khi Tiến viết xong, mở app, nhập đúng 3 dòng này, quantum 2, bấm RUN
mà ra đúng bảng này thì code đúng. Ra khác là code sai, báo nhóm trưởng.

## Nộp bài lên GitHub — mỗi người, mỗi ngày

1. Clone repo một lần duy nhất.
2. Tạo nhánh của mình: `git checkout -b dev/<ten-khong-dau>`
3. Làm xong thì commit bằng đúng tên mình:

```text
git add .
git commit -m "ghi rõ đã làm gì"
git push origin dev/<ten-khong-dau>
```

4. Lên GitHub tạo Pull Request về nhánh `main`, chờ nhóm trưởng merge.
   Không push thẳng lên `main`.
5. Mỗi ngày ít nhất 1 commit có nội dung thật. Thầy xem lịch sử commit
   để chấm đóng góp, không có commit là không có điểm phần đó.

## Kẹt thì hỏi ai

Hỏi nhóm trưởng (Khang). Đừng tự đoán rồi sửa lung tung sang phần của
người khác.
