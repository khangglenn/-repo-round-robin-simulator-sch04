# Giao dien mo phong Round Robin (Tkinter, chi dung thu vien co san)
# De tai OS_SCH_04 - Nhom OS_2627102_01 - Mon He dieu hanh, UTH
# Logic tinh toan nam o file rr_engine.py, file nay chi lo man hinh.
# Chay: python src/main.py (Python 3.10 tro len, khong can cai them gi)

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Them thu muc src vao duong dan de import duoc rr_engine
# khi chay tu thu muc goc bang lenh python src/main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rr_engine import (Process, compare_quanta, load_processes_csv,
                       save_results_csv, simulate_round_robin)

# Mau cho tung tien trinh tren bieu do Gantt
COLORS = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
          "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"]
# Thu muc goc cua project (thu muc cha cua src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Round Robin Simulator - OS_SCH_04 - Nhom OS_2627102_01")
        self.geometry("1080x720")
        self.processes = []   # danh sach tien trinh dang nhap
        self.last_result = None  # ket qua mo phong gan nhat
        self._build_ui()
        self._load_sample()

    # ---------- Ve man hinh ----------
    def _build_ui(self):
        # Khung ben trai: nhap lieu
        left = ttk.Frame(self, padding=8)
        left.pack(side="left", fill="y")

        ttk.Label(left, text="Processes (pid, arrival, burst)").pack(anchor="w")
        self.table = ttk.Treeview(left, columns=("pid", "arr", "burst"),
                                  show="headings", height=9)
        self.table.heading("pid", text="PID")
        self.table.heading("arr", text="Arrival")
        self.table.heading("burst", text="Burst")
        self.table.column("pid", width=60, anchor="center")
        self.table.column("arr", width=70, anchor="center")
        self.table.column("burst", width=70, anchor="center")
        self.table.pack()

        # O nhap tien trinh moi
        form = ttk.Frame(left)
        form.pack(pady=6)
        self.e_pid = ttk.Entry(form, width=6)
        self.e_arr = ttk.Entry(form, width=6)
        self.e_burst = ttk.Entry(form, width=6)
        self.e_pid.pack(side="left", padx=2)
        self.e_arr.pack(side="left", padx=2)
        self.e_burst.pack(side="left", padx=2)
        ttk.Button(form, text="Add", command=self.add_process).pack(side="left")
        ttk.Button(form, text="Remove selected",
                   command=self.remove_process).pack(side="left", padx=2)

        ttk.Button(left, text="Load CSV input...",
                   command=self.load_csv).pack(fill="x", pady=2)
        ttk.Separator(left).pack(fill="x", pady=6)

        # Chon quantum va thoi gian doi nguoi
        self.var_q = tk.IntVar(value=2)
        self.var_cs = tk.IntVar(value=0)
        row = ttk.Frame(left)
        row.pack(anchor="w")
        ttk.Label(row, text="Time quantum:").pack(side="left")
        ttk.Spinbox(row, from_=1, to=50, textvariable=self.var_q,
                    width=5).pack(side="left", padx=4)
        row2 = ttk.Frame(left)
        row2.pack(anchor="w", pady=2)
        ttk.Label(row2, text="Context-switch time:").pack(side="left")
        ttk.Spinbox(row2, from_=0, to=10, textvariable=self.var_cs,
                    width=5).pack(side="left", padx=4)
        ttk.Button(left, text="RUN SIMULATION",
                   command=self.run).pack(fill="x", pady=8)
        ttk.Button(left, text="Save results CSV...",
                   command=self.save_csv).pack(fill="x")

        # So sanh nhieu quantum
        ttk.Separator(left).pack(fill="x", pady=6)
        ttk.Label(left, text="Compare quanta (comma separated):").pack(anchor="w")
        self.e_quanta = ttk.Entry(left)
        self.e_quanta.insert(0, "1, 2, 3, 4, 5, 10")
        self.e_quanta.pack(fill="x")
        ttk.Button(left, text="Compare", command=self.compare).pack(fill="x", pady=4)

        # Khung ben phai: ket qua
        right = ttk.Frame(self, padding=8)
        right.pack(side="left", fill="both", expand=True)
        ttk.Label(right, text="Gantt chart").pack(anchor="w")
        self.gantt = tk.Canvas(right, height=90, bg="white")
        self.gantt.pack(fill="x")
        self.lbl_summary = ttk.Label(right, text="")
        self.lbl_summary.pack(anchor="w", pady=4)

        ttk.Label(right, text="Per-process results").pack(anchor="w")
        cols = ("pid", "arr", "burst", "comp", "tat", "wait", "resp")
        titles = ("PID", "Arrival", "Burst", "Completion",
                  "Turnaround", "Waiting", "Response")
        self.results = ttk.Treeview(right, columns=cols, show="headings",
                                    height=7)
        for i in range(len(cols)):
            self.results.heading(cols[i], text=titles[i])
            self.results.column(cols[i], width=90, anchor="center")
        self.results.pack(fill="x")

        ttk.Label(right, text="Effect of the time quantum").pack(anchor="w",
                                                                 pady=(8, 0))
        ccols = ("q", "wait", "tat", "resp", "switches", "overhead", "total")
        ctitles = ("Quantum", "Avg waiting", "Avg turnaround",
                   "Avg response", "Switches", "Overhead", "Total time")
        self.compare_table = ttk.Treeview(right, columns=ccols,
                                          show="headings", height=6)
        for i in range(len(ccols)):
            self.compare_table.heading(ccols[i], text=ctitles[i])
            self.compare_table.column(ccols[i], width=100, anchor="center")
        self.compare_table.pack(fill="x")

    # ---------- Ham phu ----------
    def _refresh_table(self):
        # Ve lai bang tien trinh tu danh sach hien tai
        self.table.delete(*self.table.get_children())
        for p in self.processes:
            self.table.insert("", "end", values=(p.pid, p.arrival, p.burst))

    def _load_sample(self):
        # Mo app len la nap san file mau, neu loi thi dung 2 tien trinh mac dinh
        try:
            self.processes = load_processes_csv(
                os.path.join(BASE_DIR, "input", "sample_01.csv"))
        except Exception:
            self.processes = [Process("P1", 0, 5), Process("P2", 1, 3)]
        self._refresh_table()

    def add_process(self):
        # Them mot tien trinh tu o nhap vao danh sach
        try:
            p = Process(self.e_pid.get().strip(),
                        int(self.e_arr.get()), int(self.e_burst.get()))
            if p.pid == "" or p.burst <= 0 or p.arrival < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input",
                                 "Check pid / arrival (>=0) / burst (>0).")
            return
        self.processes.append(p)
        self._refresh_table()

    def remove_process(self):
        # Xoa tien trinh dang chon trong bang
        sel = self.table.selection()
        if len(sel) > 0:
            idx = self.table.index(sel[0])
            self.processes.pop(idx)
            self._refresh_table()

    def load_csv(self):
        # Chon file CSV de nap danh sach tien trinh
        path = filedialog.askopenfilename(
            initialdir=os.path.join(BASE_DIR, "input"),
            filetypes=[("CSV files", "*.csv")])
        if path != "":
            self.processes = load_processes_csv(path)
            self._refresh_table()

    def save_csv(self):
        # Luu bang ket qua ra file CSV, phai chay mo phong truoc
        if self.last_result is None:
            messagebox.showinfo("Nothing to save", "Run the simulation first.")
            return
        path = filedialog.asksaveasfilename(
            initialdir=os.path.join(BASE_DIR, "output"),
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path != "":
            save_results_csv(path, self.last_result)

    # ---------- Mo phong ----------
    def run(self):
        # Chay mo phong voi quantum va thoi gian doi nguoi dang chon
        if len(self.processes) == 0:
            messagebox.showinfo("No processes", "Add at least one process.")
            return
        r = simulate_round_robin(self.processes, self.var_q.get(),
                                 self.var_cs.get())
        self.last_result = r
        # Dien bang ket qua tung tien trinh
        self.results.delete(*self.results.get_children())
        for x in r.per_process:
            self.results.insert("", "end", values=(
                x.pid, x.arrival, x.burst, x.completion,
                x.turnaround, x.waiting, x.response))
        # Dong tom tat cac gia tri trung binh
        self.lbl_summary.config(text=(
            "Avg waiting: " + format(r.avg_waiting, ".2f") +
            "   Avg turnaround: " + format(r.avg_turnaround, ".2f") +
            "   Avg response: " + format(r.avg_response, ".2f") +
            "   Context switches: " + str(r.context_switches) +
            "   Overhead: " + str(r.overhead_time) +
            "   Total time: " + str(r.total_time)))
        self._draw_gantt(r)

    def _draw_gantt(self, r):
        # Ve bieu do Gantt tu danh sach doan
        c = self.gantt
        c.delete("all")
        width = c.winfo_width()
        if width < 600:
            width = 600
        unit = (width - 20) / max(r.total_time, 1)
        # Gan moi tien trinh mot mau
        color = {}
        i = 0
        for p in self.processes:
            color[p.pid] = COLORS[i % len(COLORS)]
            i = i + 1
        for s in r.segments:
            x0 = 10 + s.start * unit
            x1 = 10 + s.end * unit
            if s.pid == "IDLE":
                fill = "#dddddd"
            elif s.pid == "CS":
                fill = "#999999"
            elif s.pid in color:
                fill = color[s.pid]
            else:
                fill = "#cccccc"
            c.create_rectangle(x0, 15, x1, 55, fill=fill, outline="black")
            if x1 - x0 > 16:
                c.create_text((x0 + x1) / 2, 35, text=s.pid)
            c.create_text(x0, 68, text=str(s.start))
        c.create_text(10 + r.total_time * unit, 68, text=str(r.total_time))

    def compare(self):
        # So sanh nhieu quantum, dien vao bang ben duoi
        if len(self.processes) == 0:
            return
        try:
            quanta = []
            for x in self.e_quanta.get().split(","):
                if x.strip() != "":
                    quanta.append(int(x))
        except ValueError:
            messagebox.showerror("Invalid list", "Example: 1, 2, 3, 4, 5")
            return
        rows = compare_quanta(self.processes, quanta, self.var_cs.get())
        self.compare_table.delete(*self.compare_table.get_children())
        for row in rows:
            self.compare_table.insert("", "end", values=(
                row["quantum"], row["avg_waiting"], row["avg_turnaround"],
                row["avg_response"], row["context_switches"],
                row["overhead_time"], row["total_time"]))


if __name__ == "__main__":
    App().mainloop()
