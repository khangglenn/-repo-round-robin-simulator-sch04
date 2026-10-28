# File nay do Huynh Minh Triet tu viet tu dau.
# Huong dan chi tiet xem trong docs/HUONG_DAN.md (muc 5).
from tkinter import *
from tkinter import messagebox, filedialog
import csv
import os

try:
    from rr_engine import simulate_round_robin, compare_quanta
except ImportError:
    simulate_round_robin = None
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
        messagebox.showerror("Error", "Nhap day du thong tin!")
        return
    try:
        arrival = int(arr)
        burst = int(bur)
        if arrival < 0 or burst <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Arrival>= 0 , Burst > 0 (so nguyen)!")
        return
        
    p = {"pid": pid, "arrival": arrival, "burst": burst}
    processes_list.append(p)
    list_processes.insert(END, f"PID: {pid} | Den: {arrival} | Chay: {burst}")
    
    e_pid.delete(0, END)
    e_arrival.delete(0, END)
    e_burst.delete(0, END)

Button(root, text="Add processes", bg="lightgreen", width=18, command=add_process).grid(row=4, column=0, columnspan=2, pady=5)

Button(root, text="Upload file CSV", bg="lightyellow", width=18).grid(row=5, column=2, padx=10, pady=5)

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

btn_frame = Frame(root)
btn_frame.grid(row=7, column=0, columnspan=3, pady=5)

Button(btn_frame, text="RUN", bg="lightblue", width=12).pack(side=LEFT, padx=10)
Button(btn_frame, text="Compare", bg="lightyellow", width=12).pack(side=LEFT, padx=10)
Button(btn_frame, text="Export", bg="lightgray", width=12).pack(side=LEFT, padx=10)

root.mainloop()