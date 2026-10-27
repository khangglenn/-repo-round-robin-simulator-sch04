# Hướng dẫn làm app Round Robin (đọc hết rồi mới gõ code, đừng đọc nửa vời)

Mình viết cái này cho cả nhóm, ai chưa biết gì cũng đọc được. Đọc hết
một lượt rồi hãy làm phần của mình. Kẹt chỗ nào thì nhắn mình, đừng
ngồi im.

## 0. App này làm cái gì

Môn Hệ điều hành bắt mình mô phỏng cách CPU chia thời gian cho nhiều
chương trình chạy cùng lúc. Thuật toán Round Robin thì đơn giản thôi:
mỗi chương trình được chạy một lúc ngắn gọi là quantum, hết lượt thì
nhường cho đứa khác, xoay vòng tới khi xong hết.

Tưởng tượng quán net có 1 máy, nhiều đứa xếp hàng chơi. Mỗi đứa chơi
2 phút rồi đứng dậy cho đứa sau, ai chưa chơi xong thì xếp lại cuối
hàng. Cái "2 phút" đó chính là quantum.

App mình làm đúng vậy: nhập danh sách tiến trình với giờ đến và thời
gian cần chạy, chọn quantum, app tính ra ai chạy lúc nào, mỗi đứa chờ
bao lâu, rồi so sánh xem quantum nào ngon hơn.

## 1. Ai làm cái gì

App có 4 file code, mỗi đứa 1 file, không đụng file của nhau:

| Người | File | Việc |
|-------|------|------|
| Tiến | `src/rr_engine.py` | Bộ não: tính toán mô phỏng. |
| Triết | `src/main.py` | Mặt tiền: cửa sổ giao diện người dùng bấm vào. |
| Long Vũ | `src/charts.py` | Vẽ biểu đồ so sánh các quantum. |
| Hải Đăng | `src/export.py` | Xuất kết quả ra file để đưa vào báo cáo. |
| Mình (nhóm trưởng) | Không giữ file code nào | Gộp code 4 đứa, viết báo cáo, slide, video, đóng gói, nộp bài. |

4 file đang rỗng, mỗi đứa tự viết từ đầu. Thầy chấm phần này kỹ lắm:
ai viết phần nào, có hiểu phần mình không, nhìn commit là biết hết.

## 2. 4 mảnh ghép với nhau như nào

Người dùng mở app (phần Triết), nhập dữ liệu hoặc tải file CSV, bấm
RUN. Giao diện gọi bộ não (phần Tiến) tính xem ai chạy lúc nào, chờ
bao lâu. Rồi giao diện hiện kết quả lên màn hình: bảng kết quả từng
tiến trình với biểu đồ Gantt (phần Triết).

Người dùng bấm Compare: bộ não chạy thử nhiều quantum khác nhau, Long
Vũ vẽ biểu đồ so sánh. Người dùng bấm Export: Hải Đăng ghi kết quả
với trace chi tiết ra file.

Cho nên Tiến phải làm trước. Triết, Long Vũ, Hải Đăng đều cần bộ não
chạy được mới làm tiếp được. Tiến ráng có bản chạy được càng sớm càng
tốt, chưa cần hoàn hảo, rồi cải tiến sau. 3 đứa kia trong lúc chờ thì
cứ làm phần mình trước bằng dữ liệu giả tự bịa, khỏi cần chờ bộ não
hoàn hảo.

## 3. Mấy cái cả nhóm phải thống nhất

Cái này quan trọng nhất. Mỗi đứa tự đặt tên khác nhau là 4 mảnh không
ráp lại được, tới lúc gộp ngồi khóc. Nên chốt hết dưới đây, muốn đổi
thì nói cả nhóm đổi theo, đừng tự đổi một mình.

### 3.1. File dữ liệu CSV

CSV là file bảng đơn giản: mỗi dòng một hàng, các cột cách nhau bằng
dấu phẩy. File dữ liệu của mình có 3 cột, dòng đầu là tiêu đề:

```
pid,arrival,burst
P1,0,5
P2,1,3
P3,2,1
```

- `pid`: tên tiến trình, ví dụ P1, P2.
- `arrival`: giờ tiến trình đến, số nguyên, từ 0 trở lên.
- `burst`: thời gian tiến trình cần chạy, số nguyên, lớn hơn 0.

### 3.2. Bộ não nhận gì, trả gì

Bộ não có 2 hàm, tên chốt như này, đừng đặt tên khác:

- `simulate_round_robin(processes, quantum, context_switch=0)`:
  nhận danh sách tiến trình, quantum, thời gian đổi lượt (mặc định 0).
  Mỗi tiến trình là một dict có 3 khóa: `pid`, `arrival`, `burst`.
  Ví dụ: `{"pid": "P1", "arrival": 0, "burst": 5}`.
  Trả về một dict có 2 phần:
  - `segments`: danh sách các đoạn chạy, mỗi đoạn là một dict có
    `pid`, `start`, `end`. `pid` là tên tiến trình, hoặc `"IDLE"` khi
    CPU rảnh vì chưa có đứa nào đến kịp, hoặc `"CS"` khi đang đổi
    lượt. Ví dụ `{"pid": "P1", "start": 0, "end": 2}` nghĩa là P1
    chạy từ giờ 0 đến giờ 2.
  - `results`: danh sách kết quả từng tiến trình, mỗi kết quả là một
    dict có các khóa: `pid`, `arrival`, `burst`, `completion` (giờ
    xong), `turnaround` (giờ xong trừ giờ đến), `waiting`
    (turnaround trừ burst), `response` (giờ chạy lần đầu trừ giờ đến).

- `compare_quanta(processes, quanta, context_switch=0)`: nhận danh
  sách tiến trình với danh sách các quantum cần so sánh, ví dụ
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
- Hải Đăng: `xuat_bang_ket_qua(result, path)` với `xuat_trace(result,
  path)` — nhận kết quả mô phỏng từ bộ não, ghi ra file ở đường dẫn
  `path`.

### 3.4. Cách import với cách chạy app

- Chạy app từ thư mục gốc của repo, gõ: `python src/main.py`
  (Windows cũng gõ đúng lệnh này).
- File trong thư mục `src/` import nhau bằng tên file trực tiếp, ví dụ
  trong `main.py` thì viết `from rr_engine import simulate_round_robin`.
  Không cần file `__init__.py`.
- Chỉ dùng thư viện có sẵn của Python (Tkinter để vẽ cửa sổ), đừng cài
  thêm thư viện lạ, vì thầy chấm trên Windows.

## 4. Phần của Tiến — bộ não (`src/rr_engine.py`)

### 4.1. Thuật toán nói bằng tiếng người

- Bước 1: xếp mấy tiến trình theo giờ đến. Đứa nào đến trước đứng
  trước. Đến cùng giờ thì giữ đúng thứ tự trong file.
- Bước 2: lấy đứa đầu hàng, cho chạy tối đa bằng quantum. Nó cần ít
  hơn hoặc bằng quantum thì chạy cho xong, ghi giờ xong. Nó cần nhiều
  hơn quantum thì chạy đúng quantum rồi xếp lại cuối hàng.
- Bước 3: trong lúc một đứa đang chạy, đứa nào đến kịp thì xếp vào
  cuối hàng.
- Bước 4: hết lượt mà trong hàng không còn ai, nhưng vẫn còn đứa chưa
  đến, thì CPU rảnh (IDLE) cho tới giờ đứa tiếp theo đến.
- Bước 5: mỗi lần đổi lượt tốn thêm thời gian context switch (nếu có),
  ghi một đoạn CS.
- Bước 6: lặp lại tới khi xong hết. Tính cho từng đứa: completion (giờ
  xong), turnaround = completion - arrival, waiting = turnaround -
  burst, response = giờ chạy lần đầu - arrival.

### 4.2. Ví dụ này bắt buộc phải ra đúng số, sai số nào là code sai

Dữ liệu: P1 đến giờ 0 cần 5, P2 đến giờ 1 cần 3, P3 đến giờ 2 cần 1,
quantum 2, thời gian đổi lượt 0.

Kết quả phải ra đúng như này:

```
P1 chạy 0–2, P2 chạy 2–4, P3 chạy 4–5, P1 chạy 5–7, P2 chạy 7–8, P1 chạy 8–9.
Thời gian chờ: P1 = 4, P2 = 4, P3 = 2.
Số lần đổi lượt: 5.
```

Nói lại một lượt cho dễ hiểu: P1 chạy 0–2 rồi hết lượt nên nhường, P2
chạy 2–4 rồi nhường, P3 chạy 4–5 là xong luôn vì chỉ cần 1, P1 quay lại
chạy 5–7 rồi nhường, P2 chạy 7–8 là xong, P1 chạy nốt 8–9 là xong.

### 4.3. Mấy trường hợp này phải lo, không là app crash

- Không có tiến trình nào: báo lỗi đàng hoàng, đừng để crash.
- Giờ đến âm, thời gian cần chạy nhỏ hơn hoặc bằng 0, quantum nhỏ hơn
  hoặc bằng 0: báo lỗi, đừng để crash.
- Tiến trình đến sau khi CPU rảnh: vẽ đoạn IDLE.
- Nhiều đứa đến cùng giờ: giữ đúng thứ tự trong file.
- Quantum lớn hơn mọi thời gian cần chạy: app chạy giống như ai đến
  trước chạy trước, không còn đổi lượt.

### 4.4. So sánh quantum

Chạy lại đúng thuật toán ở mục 4.1 với từng quantum trong danh sách,
tính trung bình các chỉ số cho mỗi quantum, trả về đúng định dạng ở
mục 3.2.

## 5. Phần của Triết — giao diện (`src/main.py`)

Cửa sổ app cần có đủ mấy thứ này, thiếu cái nào là trừ điểm:

- Chỗ tải file CSV (nút Load CSV) với bảng hiện danh sách tiến trình
  vừa tải, hoặc chỗ nhập tay từng tiến trình.
- Ô nhập quantum, ô nhập thời gian đổi lượt (context switch).
- Nút RUN: gọi bộ não của Tiến, hiện bảng kết quả từng tiến trình
  (pid, giờ đến, thời gian cần chạy, giờ xong, turnaround, waiting,
  response) rồi vẽ biểu đồ Gantt: mỗi đoạn chạy là một ô màu, ghi tên
  tiến trình với giờ bắt đầu, giờ kết thúc.
- Nút Compare: cho nhập nhiều quantum (ví dụ 1, 2, 5, 10), hiện bảng
  so sánh, rồi gọi hàm vẽ biểu đồ của Long Vũ.
- Nút Export: gọi hàm xuất file của Hải Đăng, lưu kết quả với trace ra
  file trong thư mục `output/`.
- Nhập sai (file sai định dạng, số âm, ô trống) thì hiện thông báo lỗi
  dễ hiểu bằng tiếng Việt, app không được crash, không được tắt đột
  ngột.
- App phải chạy được trên Windows: chỉ dùng Tkinter có sẵn, đường dẫn
  file đừng có ký tự đặc biệt, chữ tiếng Việt hiện đúng dấu.
- Lúc đầu chưa có bộ não thì cứ làm giao diện trước bằng dữ liệu giả
  tự bịa, khi nào bộ não chạy được thì nối vào sau.

## 6. Phần của Long Vũ — biểu đồ (`src/charts.py`)

- Nhận danh sách các dòng kết quả từ hàm `compare_quanta` của Tiến.
- Vẽ 3 biểu đồ:
  - Thời gian chờ trung bình theo quantum.
  - Thời gian đáp ứng trung bình theo quantum.
  - Số lần đổi lượt theo quantum.
- Mỗi biểu đồ phải có tên trục, đơn vị, chú thích rõ ràng, nhìn vào là
  biết ngay quantum nào ngon hơn, quantum nào tệ hơn.
- Xuất hình ra file để đưa vào báo cáo với slide (gợi ý: vẽ bằng
  Canvas của Tkinter rồi xuất file hình bằng hàm postscript của
  Canvas).
- Chỉ dùng thư viện có sẵn, đừng cài thêm.
- Lúc đầu chưa có bộ não thì cứ vẽ trước bằng dữ liệu giả tự bịa theo
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
- Nhớ phân biệt: bảng chữ với trace này khác với file CSV thô. File
  CSV thô chỉ là dữ liệu dạng bảng cho máy đọc, còn 2 file này là để
  người đọc trong báo cáo.
- Lúc đầu chưa có bộ não thì cứ xuất trước bằng dữ liệu giả tự bịa
  theo đúng định dạng ở mục 3.2, khi nào bộ não chạy được thì nối vào
  sau.

## 8. Git làm sao — làm đúng thứ tự, đừng sáng tạo

Mấy từ này ai chưa biết thì đọc trước:

- Repo: kho code chung của nhóm trên GitHub.
- Nhánh (branch): bản làm riêng của mỗi đứa, làm trên nhánh mình thì
  không đụng vào code của ai.
- Commit: một lần lưu việc đã làm, kèm lời mô tả ngắn.
- Pull Request: đơn xin gộp nhánh của mình vào nhánh chính (main).

Rồi làm đúng thứ tự:

1. Cài Git với Python 3.10 trở lên trên máy mình.
2. Clone repo về máy (chỉ làm một lần duy nhất):
   `git clone https://github.com/khangglenn/-repo-round-robin-simulator-sch04`
3. Tạo nhánh riêng của mình (chỉ làm một lần duy nhất):
   `git checkout -b dev/tên-mình` (ví dụ Tiến là `dev/tien`, Triết là
   `dev/triet`). Từ giờ chỉ làm trên nhánh này, đừng đụng vào nhánh
   main.
4. Mở file của mình, viết code, lưu.
5. Lưu một lần làm việc:
   `git add .` rồi `git commit -m "mô tả ngắn việc vừa làm"` rồi
   `git push origin dev/tên-mình`.
6. Lên GitHub, bấm Compare & pull request, chọn gộp về nhánh main,
   chờ mình review rồi gộp.
7. Mỗi ngày ít nhất 1 commit có nội dung thật. Đừng push thẳng lên
   main, đừng tự gộp code của người khác.
8. Trước khi làm tiếp ngày hôm sau, lấy code mới nhất của nhóm về
   nhánh mình: `git checkout main`, `git pull`, rồi `git checkout
   dev/tên-mình`, `git merge main`.

## 9. Trước khi gửi Pull Request thì tự check mấy cái này

- Chạy ví dụ ở mục 4.2, số phải khớp y hệt từng con số.
- Thử mấy trường hợp: không có tiến trình, nhập sai số, quantum bằng
  0, CPU rảnh vì chưa ai đến.
- App không crash với bất kỳ dữ liệu hợp lệ nào. Dữ liệu sai thì báo
  lỗi đàng hoàng bằng tiếng Việt.
- Code chạy được bằng Python có sẵn, khỏi cần cài thêm gì.
- File của mình chỉ làm đúng phần của mình, đừng sửa file của người
  khác.

## 10. Mấy từ mới, ai chưa biết thì đọc

- Repo: kho code chung trên GitHub.
- Branch (nhánh): bản làm riêng của mỗi đứa.
- Commit: một lần lưu việc đã làm, kèm lời mô tả.
- Pull Request: đơn xin gộp nhánh mình vào nhánh chính.
- CSV: file bảng đơn giản, mỗi dòng một hàng, các cột cách nhau bằng
  dấu phẩy.
- Gantt: biểu đồ thanh ngang cho thấy ai chạy lúc nào.
- Quantum: khoảng thời gian tối đa mỗi lượt chạy.
- Context switch: thời gian tốn khi đổi từ tiến trình này sang tiến
  trình khác.
- Turnaround: giờ xong trừ giờ đến. Waiting: turnaround trừ thời gian
  cần chạy. Response: giờ chạy lần đầu trừ giờ đến.
- Trace: nhật ký chi tiết từng bước chạy, ai chạy lúc nào.

## 11. Thứ tự làm việc với mốc chung

1. Tiến làm bộ não trước, có bản chạy được càng sớm càng tốt.
2. Triết, Long Vũ, Hải Đăng làm tiếp khi bộ não chạy được (lúc đầu cứ
   làm bằng dữ liệu giả tự bịa, khỏi cần chờ bộ não hoàn hảo).
3. Mình gộp code, viết báo cáo, slide, video, đóng gói, nộp bài.
4. Mốc chung của nhóm: code xong 31/10, phân tích xong 04/11, báo cáo
   với slide với video xong 07/11, nộp thử 08/11, hạn thật 09/11 lúc
   23:59.
5. Kẹt thì nhắn mình ngay, đừng im tới sát hạn mới nói.
