# File nay do Nguyen Long Vu tu viet tu dau.
# Huong dan chi tiet xem trong docs/HUONG_DAN.md (muc 6).

import os
import tkinter as tk

def ve_bieu_do_so_sanh(rows, parent=None):
    if not rows:
        print("Không có dữ liệu để vẽ biểu đồ.")
        return

    if parent:
        root = tk.Toplevel(parent)
    else:
        root = tk.Toplevel() #tạo không gian vẽ khung
    root.title("Biểu đồ so sánh Round Robin.")

    configs = [
        ("1. THỜI GIAN CHỜ TRUNG BÌNH THEO QUANTUM", "avg_waiting", "(Thời gian)", "skyblue", "bieu_do_cho_trung_binh.eps"),
        ("2. THỜI GIAN ĐÁP ỨNG TRUNG BÌNH THEO QUANTUM", "avg_response", "(Thời gian)", "lightgreen", "bieu_do_dap_ung_trung_binh.eps"),
        ("3. SỐ LẦN CHUYỂN NGỮ CẢNH THEO QUANTUM", "context_switches", "(Số lần)", "orange", "bieu_do_chuyen_ngu_canh.eps")
    ]

    for title, key, y_label, color, filename in configs:
        width, height = 700, 250
        canvas = tk.Canvas(root, width=width, height=height, bg="white")
        canvas.pack()

        canvas.create_text(width / 2, 30, text=title, font=("Arial", 12, "bold")) #title

        margin_left, margin_right = 70, 50  #tọa độ, lề
        margin_top, margin_bottom = 70, 70

        chart_w = width - margin_left - margin_right
        chart_h = height - margin_top - margin_bottom

        canvas.create_line(margin_left, margin_top, margin_left, height - margin_bottom, width=2) #trục
        canvas.create_line(margin_left, height - margin_bottom, width - margin_right, height - margin_bottom, width=2)

        canvas.create_text(margin_left - 30, margin_top - 15, text=y_label, font=("Arial", 9, "bold"))
        canvas.create_text(width / 2, height - margin_bottom + 45, text="Quantum (q)", font=("Arial", 10, "bold"))

        max_val = max(r.get(key, 0) for r in rows)
        if max_val == 0:
            max_val = 1

        n = len(rows)
        bar_w = min(45, chart_w / (n * 2))
        gap = (chart_w - n * bar_w) / (n + 1)

        for i, r in enumerate(rows):
            q = r.get("quantum", 0)
            val = r.get(key, 0)

            x0 = margin_left + gap + i * (bar_w + gap)
            x1 = x0 + bar_w

            bar_h = (val / max_val) * (chart_h - 20)
            y1 = height - margin_bottom
            y0 = y1 - bar_h

            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
            canvas.create_text((x0 + x1) / 2, y0 - 10, text=f"{val:.1f}", font=("Arial", 9, "bold"))
            canvas.create_text((x0 + x1) / 2, y1 + 15, text=f"q={q}", font=("Arial", 9))

        os.makedirs("output", exist_ok=True)
        canvas.update()
        output_path = f"output/{filename}"
        canvas.postscript(file=output_path)
        print(f"Đã xuất biểu đồ ra file: {output_path}") #xuất file về thư mục

if __name__ == "__main__":
    fake_data = [
        {"quantum": 1, "avg_waiting": 5.5, "avg_response": 1.5, "context_switches": 10},
        {"quantum": 2, "avg_waiting": 4.0, "avg_response": 2.0, "context_switches": 5},
        {"quantum": 5, "avg_waiting": 3.0, "avg_response": 3.0, "context_switches": 2}
    ]

    test_root = tk.Tk()
    test_root.withdraw()
    ve_bieu_do_so_sanh(fake_data, parent=test_root)
    test_root.mainloop()