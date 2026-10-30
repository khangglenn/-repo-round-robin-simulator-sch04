# File nay do Huynh Minh Triet tu viet tu dau.
# Huong dan chi tiet xem trong docs/HUONG_DAN.md (muc 5).
from tkinter import *
from tkinter import messagebox, filedialog
import csv
import os

try:
    from rr_engine import simulate_round_robin
except ImportError:
    simulate_round_robin = None

try:
    from rr_engine import compare_quanta
except ImportError:
    compare_quanta = None

try:
    from charts import ve_bieu_do_so_sanh
except ImportError:
    ve_bieu_do_so_sanh = None

try:
    from export import xuat_bang_ket_qua, xuat_trace
except ImportError:
    xuat_bang_ket_qua = None
    xuat_trace = None

root = Tk()
root.title("Round Robin")
root.geometry("750x650")
root.minsize(700, 600)

processes_list = []

Label(root, text="THUẬT TOÁN ROUND ROBIN", fg="blue", font=("Cambria", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

Label(root, text="PID :").grid(row=1, column=0, sticky=W, padx=10, pady=2)
e_pid = Entry(root, width=20)
e_pid.grid(row=1, column=1, sticky=W, pady=2)

Label(root, text="Arrival :").grid(row=2, column=0, sticky=W, padx=10, pady=2)
e_arrival = Entry(root, width=20)
e_arrival.grid(row=2, column=1, sticky=W, pady=2)

Label(root, text="Burst :").grid(row=3, column=0, sticky=W, padx=10, pady=2)
e_burst = Entry(root, width=20)
e_burst.grid(row=3, column=1, sticky=W, pady=2)

list_processes = Listbox(root, width=35, height=6)
list_processes.grid(row=1, column=2, rowspan=4, padx=10)

def add_process():
    pid = e_pid.get().strip()
    arr = e_arrival.get().strip()
    bur = e_burst.get().strip()
    
    if not pid or not arr or not bur:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin tiến trình!")
        return
    try:
        arrival = int(arr)
        burst = int(bur)
        if arrival < 0 or burst <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Lỗi", "Yêu cầu: Arrival >= 0 và Burst > 0 (số nguyên)!")
        return
        
    p = {"pid": pid, "arrival": arrival, "burst": burst}
    processes_list.append(p)
    list_processes.insert(END, f"PID: {pid} | Đến: {arrival} | Chạy: {burst}")
    
    e_pid.delete(0, END)
    e_arrival.delete(0, END)
    e_burst.delete(0, END)

Button(root, text="Thêm tiến trình", bg="lightgreen", width=18, command=add_process).grid(row=4, column=0, columnspan=2, pady=5)

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    try:
        global processes_list
        processes_list = []
        list_processes.delete(0, END)
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = {
                    "pid": row["pid"].strip(),
                    "arrival": int(row["arrival"].strip()),
                    "burst": int(row["burst"].strip())
                }
                processes_list.append(p)
                list_processes.insert(END, f"PID: {p['pid']} | Đến: {p['arrival']} | Chạy: {p['burst']}")
        messagebox.showinfo("Thành công", "Đã tải file CSV thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc file CSV: {e}")

Button(root, text="Tải file CSV", bg="lightyellow", width=18, command=load_csv).grid(row=5, column=2, padx=10, pady=5)

Label(root, text="Time Quantum:").grid(row=5, column=0, sticky=W, padx=10, pady=5)
e_quantum = Entry(root, width=20)
e_quantum.grid(row=5, column=1, sticky=W, pady=5)
e_quantum.insert(0, "2")

Label(root, text="Context Switch:").grid(row=6, column=0, sticky=W, padx=10, pady=5)
e_cs = Entry(root, width=20)
e_cs.grid(row=6, column=1, sticky=W, pady=5)
e_cs.insert(0, "0")

txt_result = Text(root, width=82, height=12)
txt_result.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

def run_simulation():
    if not processes_list:
        messagebox.showerror("Lỗi", "Chưa có tiến trình nào được thêm hoặc tải từ CSV!")
        return
    try:
        quantum = int(e_quantum.get().strip())
        cs = int(e_cs.get().strip())
        if quantum <= 0 or cs < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Lỗi", "Quantum > 0 và Context Switch >= 0!")
        return

    if simulate_round_robin is None:
        messagebox.showerror("Lỗi", "Chưa tìm thấy hàm `simulate_round_robin` trong `src/rr_engine.py`!")
        return

    try:
        output = simulate_round_robin(processes_list, quantum, cs)
        segments = output["segments"]
        results = output["results"]

        txt_result.delete("1.0", END)
        txt_result.insert(END, "=== KẾT QUẢ MÔ PHỎNG ROUND ROBIN ===\n")
        txt_result.insert(END, f"Các đoạn chạy (Segments): {segments}\n\n")
        txt_result.insert(END, f"{'PID':<6} | {'Arrival':<8} | {'Burst':<6} | {'Complete':<9} | {'Turnaround':<11} | {'Waiting':<8} | {'Response'}\n")
        txt_result.insert(END, "-"*75 + "\n")
        for r in results:
            txt_result.insert(END, f"{r['pid']:<6} | {r['arrival']:<8} | {r['burst']:<6} | {r['completion']:<9} | {r['turnaround']:<11} | {r['waiting']:<8} | {r['response']}\n")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy thuật toán: {e}")

def run_compare():
    if not processes_list:
        messagebox.showerror("Lỗi", "Chưa có tiến trình để so sánh!")
        return
    if compare_quanta is None:
        messagebox.showerror("Lỗi", "Chưa tìm thấy hàm `compare_quanta` trong `src/rr_engine.py`!")
        return
    
    quanta = [1, 2, 4, 8]
    try:
        cs = int(e_cs.get().strip())
        rows = compare_quanta(processes_list, quanta, cs)
        
        txt_result.delete("1.0", END)
        txt_result.insert(END, "=== SO SÁNH CÁC QUANTUM ===\n")
        for r in rows:
            txt_result.insert(END, f"Quantum: {r['quantum']} | TB Chờ: {r['avg_waiting']:.2f} | TB Hoàn thành: {r['avg_turnaround']:.2f} | Đổi lượt: {r['context_switches']}\n")
        
        if ve_bieu_do_so_sanh is not None:
            ve_bieu_do_so_sanh(rows)
            messagebox.showinfo("Thành công", "Đã gọi hàm vẽ biểu đồ so sánh thành công!")
        else:
            messagebox.showwarning("Cảnh báo", "Đã tính toán xong nhưng chưa tìm thấy module `charts.py` để vẽ biểu đồ!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi so sánh: {e}")

def run_export():
    if simulate_round_robin is None:
        messagebox.showerror("Lỗi", "Chưa có hàm `simulate_round_robin` để xuất file!")
        return
    try:
        quantum = int(e_quantum.get().strip())
        cs = int(e_cs.get().strip())
        result = simulate_round_robin(processes_list, quantum, cs)
        
        os.makedirs("output", exist_ok=True)
        if xuat_bang_ket_qua:
            xuat_bang_ket_qua(result, "output/result_table.txt")
        if xuat_trace:
            xuat_trace(result, "output/trace.txt")
            
        if xuat_bang_ket_qua or xuat_trace:
            messagebox.showinfo("Thành công", "Đã xuất kết quả ra thư mục output/ thành công!")
        else:
            messagebox.showwarning("Cảnh báo", "Chưa tìm thấy module `export.py` để xuất file!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi xuất file: {e}")

btn_frame = Frame(root)
btn_frame.grid(row=7, column=0, columnspan=3, pady=5)

Button(btn_frame, text="RUN", bg="lightblue", width=12, command=run_simulation).pack(side=LEFT, padx=10)
Button(btn_frame, text="Compare", bg="lightyellow", width=12, command=run_compare).pack(side=LEFT, padx=10)
Button(btn_frame, text="Export", bg="lightgray", width=12, command=run_export).pack(side=LEFT, padx=10)

root.mainloop()