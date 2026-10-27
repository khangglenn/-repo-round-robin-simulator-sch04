# HƯỚNG DẪN LÀM APP ROUND ROBIN — ĐỌC TỪ ĐẦU ĐẾN CUỐI RỒI HÃY GÕ CODE

Tài liệu này viết cho người mới bắt đầu, chưa biết gì về làm việc nhóm
hay về thuật toán cũng đọc được. Đọc hết một lượt rồi mới bắt tay vào
phần của mình. Kẹt chỗ nào thì hỏi nhóm trưởng (Khang), đừng ngồi im.

## 0. App này để làm gì — nói ngắn gọn nhất

Môn Hệ điều hành dạy cách máy tính chia thời gian CPU cho nhiều chương
trình cùng chạy. Thuật toán Round Robin chia theo lượt: mỗi chương trình
được chạy một khoảng ngắn gọi là time quantum, hết lượt thì nhường cho
chương trình khác, cứ xoay vòng cho đến khi tất cả xong.

Ví dụ đời thường: quán net có 1 máy, nhiều người xếp hàng chơi. Mỗi
người chơi 2 phút rồi đứng dậy cho người tiếp theo, ai chưa chơi xong
thì xếp lại cuối hàng. "2 phút" đó chính là quantum.

App của nhóm làm đúng việc đó trên máy tính: người dùng nhập danh sách
chương trình (gọi là tiến trình) với giờ đến và thời gian cần chạy,
chọn quantum, app mô phỏng và cho thấy ai chạy lúc nào, mỗi người phải
chờ bao lâu, rồi so sánh xem quantum nào tốt hơn.

## 1. Cả app có 4 file code, mỗi người 1 file

| Người | File | Việc |
|-------|------|------|
| Tiến | `src/rr_engine.py` | Bộ não: tính toán mô phỏng. |
| Triết | `src/main.py` | Mặt tiền: cửa sổ giao diện người dùng bấm vào. |
| Long Vũ | `src/charts.py` | Vẽ biểu đồ so sánh các quantum. |
| Hải Đăng | `src/export.py` | Xuất kết quả ra file để đưa vào báo cáo. |
| Khang (nhóm trưởng) | Không giữ file code nào | Gộp code của 4 người, viết báo cáo, slide, video, đóng gói, nộp bài. |

Quy tắc: 4 file hiện đang rỗng, mỗi người tự viết file của mình từ
đầu, không chép code có sẵn. Phần này là phần thầy chấm: thầy xem ai
viết phần nào, và mỗi người có hiểu phần mình viết không.

## 2. 4 mảnh ghép với nhau như thế nào

- Người dùng mở app (phần của Triết), nhập dữ liệu hoặc tải file CSV,
  bấm RUN.
- Giao diện gọi bộ não (phần của Tiến) để tính: ai chạy lúc nào, chờ
  bao lâu.
- Giao diện hiện kết quả lên màn hình: bảng kết quả từng tiến trình và
  biểu đồ Gantt (phần của Triết).
- Người dùng bấm Compare: bộ não chạy thử nhiều quantum khác nhau,
  Long Vũ vẽ biểu đồ so sánh.
- Người dùng bấm Export: Hải Đăng ghi kết quả và trace chi tiết ra file.

Vì vậy Tiến phải làm trước: Triết, Long Vũ, Hải Đăng đều cần bộ não
chạy được mới làm tiếp được. Tiến cố gắng có bản chạy được càng sớm
càng tốt, chưa cần hoàn hảo, rồi cải tiến sau. 3 người kia trong lúc
chờ thì làm phần của mình trước bằng dữ liệu giả tự tạo, không cần chờ
bộ não hoàn hảo.

## 3. Quy ước chung — cả nhóm phải theo đúng, không tự đổi

Nếu mỗi người tự đặt tên khác nhau thì 4 mảnh không ráp lại được, nên
cả nhóm thống nhất các quy ước dưới đây. Muốn đổi quy ước thì báo cả
nhóm đổi theo, không tự đổi một mình.

### 3.1. Dữ liệu vào: file CSV

File CSV là file bảng tính đơn giản: mỗi dòng là một hàng, các cột cách
nhau bằng dấu phẩy. File dữ liệu của app có 3 cột, dòng đầu tiên là
tiêu đề:

```
pid,arrival,burst
P1,0,5
P2,1,3
P3,2,1
```

- `pid`: tên tiến trình, ví dụ P1, P2.
- `arrival`: giờ tiến trình đến, số nguyên, lớn hơn hoặc bằng 0.
- `burst`: thời gian tiến trình cần chạy, số nguyên, lớn hơn 0.

### 3.2. Bộ não nhận gì, trả gì

Bộ não có 2 hàm chính, cả nhóm thống nhất tên như sau:

- `simulate_round_robin(processes, quantum, context_switch=0)`:
  nhận danh sách tiến trình, quantum, thời gian đổi lượt (mặc định 0).
  Mỗi tiến trình trong danh sách là một dict có 3 khóa: `pid`,
  `arrival`, `burst`. Ví dụ: `{"pid": "P1", "arrival": 0, "burst": 5}`.
  Trả về một dict có 2 phần:
  - `segments`: danh sách các đoạn chạy, mỗi đoạn là một dict có
    `pid`, `start`, `end`. `pid` là tên tiến trình, hoặc `"IDLE"` khi
    CPU rảnh vì chưa có tiến trình nào đến kịp, hoặc `"CS"` khi đang
    đổi lượt. Ví dụ: `{"pid": "P1", "start": 0, "end": 2}` nghĩa là
    P1 chạy từ giờ 0 đến giờ 2.
  - `results`: danh sách kết quả từng tiến trình, mỗi kết quả là một
    dict có các khóa: `pid`, `arrival`, `burst`, `completion` (giờ
    xong), `turnaround` (giờ xong trừ giờ đến), `waiting`
    (turnaround trừ burst), `response` (giờ chạy lần đầu trừ giờ đến).

- `compare_quanta(processes, quanta, context_switch=0)`: nhận danh
  sách tiến trình và danh sách các quantum cần so sánh, ví dụ
  `[1, 2, 5, 10]`. Trả về một dòng kết quả cho mỗi quantum, mỗi dòng là
  một dict có các khóa: `quantum`, `avg_waiting` (thời gian chờ trung
  bình), `avg_turnaround` (thời gian hoàn thành trung bình),
  `avg_response` (thời gian đáp ứng trung bình), `context_switches`
  (số lần đổi lượt), `overhead_time` (tổng thời gian đổi lượt, bằng số
  lần đổi lượt nhân với thời gian đổi lượt), `total_time` (giờ kết thúc
  của đoạn chạy cuối cùng).

### 3.3. Tên hàm của Long Vũ và Hải Đăng

- Long Vũ: `ve_bieu_do_so_sanh(rows)` — nhận danh sách các dòng kết
  quả từ `compare_quanta`, vẽ biểu đồ, lưu thành file hình.
- Hải Đăng: `xuat_bang_ket_qua(result, path)` và `xuat_trace(result,
  path)` — nhận kết quả mô phỏng từ bộ não, ghi ra file ở đường dẫn
  `path`.

### 3.4. Cách import và cách chạy app

- Chạy app từ thư mục gốc của repo bằng lệnh: `python src/main.py`
  (trên Windows cũng gõ đúng lệnh này).
- Các file trong thư mục `src/` import nhau bằng tên file trực tiếp,
  ví dụ trong `main.py` thì viết `from rr_engine import
  simulate_round_robin`. Không cần file `__init__.py`.
- Chỉ dùng thư viện có sẵn của Python (Tkinter để vẽ cửa sổ), không
  cài thêm thư viện lạ, vì app phải chạy được trên Windows của thầy.

## 4. Phần của Tiến — bộ não (`src/rr_engine.py`)

### 4.1. Thuật toán Round Robin, nói bằng lời

- Bước 1: xếp các tiến trình theo giờ đến. Ai đến trước đứng trước.
  Đến cùng giờ thì giữ đúng thứ tự trong file.
- Bước 2: lấy tiến trình đầu hàng, cho chạy tối đa bằng quantum. Nếu
  nó cần ít hơn hoặc bằng quantum thì chạy cho xong, ghi giờ xong.
  Nếu nó cần nhiều hơn quantum thì chạy đúng quantum rồi xếp lại cuối
  hàng.
- Bước 3: trong lúc một tiến trình chạy, tiến trình nào đến kịp thì
  xếp vào cuối hàng.
- Bước 4: hết lượt mà trong hàng không còn ai, nhưng vẫn còn tiến trình
  chưa đến, thì CPU rảnh (IDLE) cho đến giờ tiến trình tiếp theo đến.
- Bước 5: mỗi lần đổi lượt tốn thêm thời gian context switch (nếu có),
  ghi một đoạn CS.
- Bước 6: lặp lại cho đến khi tất cả xong. Tính cho từng tiến trình:
  completion (giờ xong), turnaround = completion - arrival, waiting =
  turnaround - burst, response = giờ chạy lần đầu - arrival.

### 4.2. Ví dụ để tự kiểm tra — ra đúng số này mới gọi là đúng

Dữ liệu: P1 đến giờ 0 cần 5, P2 đến giờ 1 cần 3, P3 đến giờ 2 cần 1,
quantum 2, thời gian đổi lượt 0.

Kết quả phải ra đúng như sau:

```
P1 chạy 0–2, P2 chạy 2–4, P3 chạy 4–5, P1 chạy 5–7, P2 chạy 7–8, P1 chạy 8–9.
Thời gian chờ: P1 = 4, P2 = 4, P3 = 2.
Số lần đổi lượt: 5.
```

Giải thích nhanh một lượt: P1 chạy 0–2 rồi hết lượt nên nhường, P2
chạy 2–4 rồi nhường, P3 chạy 4–5 là xong luôn vì chỉ cần 1, P1 quay
lại chạy 5–7 rồi nhường, P2 chạy 7–8 là xong, P1 chạy nốt 8–9 là xong.

### 4.3. Các trường hợp phải xử lý, không được để app crash

- Không có tiến trình nào: báo lỗi đàng hoàng, không crash.
- Giờ đến âm, thời gian cần chạy nhỏ hơn hoặc bằng 0, quantum nhỏ hơn
  hoặc bằng 0: báo lỗi, không crash.
- Tiến trình đến sau khi CPU rảnh: vẽ đoạn IDLE.
- Nhiều tiến trình đến cùng giờ: giữ đúng thứ tự trong file.
- Quantum lớn hơn mọi thời gian cần chạy: app chạy giống như ai đến
  trước chạy trước, không còn đổi lượt.

### 4.4. So sánh quantum

Chạy lại đúng thuật toán ở mục 4.1 với từng quantum trong danh sách,
tính trung bình các chỉ số cho mỗi quantum, trả về đúng định dạng ở
mục 3.2.

## 5. Phần của Triết — giao diện (`src/main.py`)

Cửa sổ app cần có đủ các thứ sau:

- Chỗ tải file CSV (nút Load CSV) và bảng hiện danh sách tiến trình
  vừa tải, hoặc chỗ nhập tay từng tiến trình.
- Ô nhập quantum, ô nhập thời gian đổi lượt (context switch).
- Nút RUN: gọi bộ não của Tiến, hiện bảng kết quả từng tiến trình
  (pid, giờ đến, thời gian cần chạy, giờ xong, turnaround, waiting,
  response) và vẽ biểu đồ Gantt: mỗi đoạn chạy là một ô màu, ghi tên
  tiến trình và giờ bắt đầu, giờ kết thúc.
- Nút Compare: cho nhập nhiều quantum (ví dụ 1, 2, 5, 10), hiện bảng
  so sánh, rồi gọi hàm vẽ biểu đồ của Long Vũ.
- Nút Export: gọi hàm xuất file của Hải Đăng, lưu kết quả và trace ra
  file trong thư mục `output/`.
- Nhập sai (file sai định dạng, số âm, ô trống) thì hiện thông báo lỗi
  dễ hiểu bằng tiếng Việt, app không được crash, không được tắt đột
  ngột.
- App phải chạy được trên Windows: chỉ dùng Tkinter có sẵn, đường dẫn
  file không chứa ký tự đặc biệt, chữ tiếng Việt hiện đúng dấu.
- Lúc đầu chưa có bộ não thì cứ làm giao diện trước bằng dữ liệu giả
  tự tạo, khi nào bộ não chạy được thì nối vào sau.

## 6. Phần của Long Vũ — biểu đồ (`src/charts.py`)

- Nhận danh sách các dòng kết quả từ hàm `compare_quanta` của Tiến.
- Vẽ 3 biểu đồ:
  - Thời gian chờ trung bình theo quantum.
  - Thời gian đáp ứng trung bình theo quantum.
  - Số lần đổi lượt theo quantum.
- Mỗi biểu đồ phải có tên trục, đơn vị, chú thích rõ ràng, nhìn vào là
  hiểu ngay quantum nào tốt hơn, quantum nào tệ hơn.
- Xuất hình ra file để đưa vào báo cáo và slide (gợi ý: vẽ bằng
  Canvas của Tkinter rồi xuất file hình bằng hàm postscript của
  Canvas).
- Chỉ dùng thư viện có sẵn, không cài thêm.
- Lúc đầu chưa có bộ não thì cứ vẽ trước bằng dữ liệu giả tự tạo theo
  đúng định dạng ở mục 3.2, khi nào bộ não chạy được thì nối vào sau.

## 7. Phần của Hải Đăng — xuất file (`src/export.py`)

- Nhận kết quả mô phỏng từ bộ não của Tiến.
- Xuất 2 file vào thư mục `output/`:
  - Bảng kết quả từng tiến trình dạng chữ, để dán thẳng vào báo cáo:
    pid, giờ đến, thời gian cần chạy, giờ xong, turnaround, waiting,
    response.
  - Trace chi tiết từng bước, làm bằng chứng cho báo cáo: mỗi dòng ghi
    ai chạy (hoặc IDLE, hoặc CS), từ giờ nào đến giờ nào. Lấy từ danh
    sách `segments` của kết quả mô phỏng.
- Chú ý: bảng chữ và trace này khác với file CSV thô. File CSV thô chỉ
  là dữ liệu dạng bảng máy đọc, còn 2 file này là để người đọc trong
  báo cáo.
- Lúc đầu chưa có bộ não thì cứ xuất trước bằng dữ liệu giả tự tạo
  theo đúng định dạng ở mục 3.2, khi nào bộ não chạy được thì nối vào
  sau.

## 8. Làm việc với Git — từng bước, ai cũng làm y hệt

- Repo: kho chứa code chung của nhóm trên GitHub.
- Nhánh (branch): bản làm việc riêng của mỗi người, làm trên nhánh
  của mình thì không đụng vào code của người khác.
- Commit: một lần lưu việc đã làm, kèm lời mô tả ngắn.
- Pull Request: đơn xin gộp nhánh của mình vào nhánh chính (main).

Các bước, làm đúng thứ tự:

1. Cài Git và Python 3.10 trở lên trên máy mình.
2. Clone repo về máy (chỉ làm một lần duy nhất):
   `git clone https://github.com/khangglenn/-repo-round-robin-simulator-sch04`
3. Tạo nhánh riêng của mình (chỉ làm một lần duy nhất):
   `git checkout -b dev/tên-mình` (ví dụ Tiến là `dev/tien`, Triết là
   `dev/triet`). Từ giờ chỉ làm trên nhánh này, không đụng vào nhánh
   main.
4. Mở file của mình, viết code, lưu.
5. Lưu một lần làm việc:
   `git add .` rồi `git commit -m "mô tả ngắn việc vừa làm"` rồi
   `git push origin dev/tên-mình`.
6. Lên GitHub, bấm Compare & pull request, chọn gộp về nhánh main,
   chờ Khang review rồi gộp.
7. Mỗi ngày ít nhất 1 commit có nội dung thật. Không push thẳng lên
   main, không tự gộp code của người khác.
8. Trước khi làm tiếp ngày hôm sau, lấy code mới nhất của nhóm về
   nhánh mình: `git checkout main`, `git pull`, rồi `git checkout
   dev/tên-mình`, `git merge main`.

## 9. Tự kiểm tra trước khi gửi Pull Request

- Chạy ví dụ ở mục 4.2, số phải khớp y hệt từng con số.
- Thử các trường hợp: không có tiến trình, nhập sai số, quantum bằng
  0, CPU rảnh vì chưa ai đến.
- App không crash với bất kỳ dữ liệu hợp lệ nào. Dữ liệu sai thì báo
  lỗi đàng hoàng bằng tiếng Việt.
- Code chạy được bằng Python có sẵn, không cần cài thêm gì.
- File của mình chỉ làm đúng phần của mình, không sửa file của người
  khác.

## 10. Từ mới giải thích nhanh

- Repo: kho code chung trên GitHub.
- Branch (nhánh): bản làm việc riêng của mỗi người.
- Commit: một lần lưu việc đã làm, kèm lời mô tả.
- Pull Request: đơn xin gộp nhánh mình vào nhánh chính.
- CSV: file bảng tính đơn giản, mỗi dòng một hàng, các cột cách nhau
  bằng dấu phẩy.
- Gantt: biểu đồ thanh ngang cho thấy ai chạy lúc nào.
- Quantum: khoảng thời gian tối đa mỗi lượt chạy.
- Context switch: thời gian tốn khi đổi từ tiến trình này sang tiến
  trình khác.
- Turnaround: giờ xong trừ giờ đến. Waiting: turnaround trừ thời gian
  cần chạy. Response: giờ chạy lần đầu trừ giờ đến.
- Trace: nhật ký chi tiết từng bước chạy, ai chạy lúc nào.

## 11. Thứ tự làm việc và mốc chung

1. Tiến làm bộ não trước, có bản chạy được càng sớm càng tốt.
2. Triết, Long Vũ, Hải Đăng làm tiếp khi bộ não chạy được (lúc đầu cứ
   làm bằng dữ liệu giả tự tạo, không cần chờ bộ não hoàn hảo).
3. Khang gộp code, viết báo cáo, slide, video, đóng gói, nộp bài.
4. Mốc chung của nhóm: code xong 31/10, phân tích xong 04/11, báo cáo
   với slide với video xong 07/11, nộp thử 08/11, hạn thật 09/11 lúc
   23:59.
5. Kẹt thì hỏi Khang ngay, đừng ngồi im tới sát hạn mới nói.
