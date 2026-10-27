"""Round Robin Simulator — GUI (Tkinter, standard library only).

Topic OS_SCH_04: Round Robin and the effect of the time quantum.
Group OS_2627102_01 — Operating Systems, UTH.

Run:  python src/main.py        (Windows / macOS / Linux, Python 3.10+)
All scheduling logic lives in rr_engine.py; this file is only the interface.
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rr_engine import (Process, compare_quanta, load_processes_csv,
                       save_results_csv, simulate_round_robin)

COLORS = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
          "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Round Robin Simulator — OS_SCH_04 — Group OS_2627102_01")
        self.geometry("1080x720")
        self.processes: list[Process] = []
        self.last_result = None
        self._build_ui()
        self._load_sample()

    # ---------- UI layout ----------
    def _build_ui(self):
        left = ttk.Frame(self, padding=8)
        left.pack(side="left", fill="y")

        ttk.Label(left, text="Processes (pid, arrival, burst)").pack(anchor="w")
        self.table = ttk.Treeview(left, columns=("pid", "arr", "burst"),
                                  show="headings", height=9)
        for col, txt, w in (("pid", "PID", 60), ("arr", "Arrival", 70),
                            ("burst", "Burst", 70)):
            self.table.heading(col, text=txt)
            self.table.column(col, width=w, anchor="center")
        self.table.pack()

        form = ttk.Frame(left)
        form.pack(pady=6)
        self.e_pid = ttk.Entry(form, width=6)
        self.e_arr = ttk.Entry(form, width=6)
        self.e_burst = ttk.Entry(form, width=6)
        for e in (self.e_pid, self.e_arr, self.e_burst):
            e.pack(side="left", padx=2)
        ttk.Button(form, text="Add", command=self.add_process).pack(side="left")
        ttk.Button(form, text="Remove selected",
                   command=self.remove_process).pack(side="left", padx=2)

        ttk.Button(left, text="Load CSV input...",
                   command=self.load_csv).pack(fill="x", pady=2)
        ttk.Separator(left).pack(fill="x", pady=6)

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

        ttk.Separator(left).pack(fill="x", pady=6)
        ttk.Label(left, text="Compare quanta (comma separated):").pack(anchor="w")
        self.e_quanta = ttk.Entry(left)
        self.e_quanta.insert(0, "1, 2, 3, 4, 5, 10")
        self.e_quanta.pack(fill="x")
        ttk.Button(left, text="Compare", command=self.compare).pack(fill="x", pady=4)

        right = ttk.Frame(self, padding=8)
        right.pack(side="left", fill="both", expand=True)
        ttk.Label(right, text="Gantt chart").pack(anchor="w")
        self.gantt = tk.Canvas(right, height=90, bg="white")
        self.gantt.pack(fill="x")
        self.lbl_summary = ttk.Label(right, text="")
        self.lbl_summary.pack(anchor="w", pady=4)

        ttk.Label(right, text="Per-process results").pack(anchor="w")
        cols = ("pid", "arr", "burst", "comp", "tat", "wait", "resp")
        self.results = ttk.Treeview(right, columns=cols, show="headings",
                                    height=7)
        for col, txt in zip(cols, ("PID", "Arrival", "Burst", "Completion",
                                   "Turnaround", "Waiting", "Response")):
            self.results.heading(col, text=txt)
            self.results.column(col, width=90, anchor="center")
        self.results.pack(fill="x")

        ttk.Label(right, text="Effect of the time quantum").pack(anchor="w",
                                                                 pady=(8, 0))
        ccols = ("q", "wait", "tat", "resp", "switches", "overhead", "total")
        self.compare_table = ttk.Treeview(right, columns=ccols,
                                          show="headings", height=6)
        for col, txt in zip(ccols, ("Quantum", "Avg waiting", "Avg turnaround",
                                    "Avg response", "Switches", "Overhead",
                                    "Total time")):
            self.compare_table.heading(col, text=txt)
            self.compare_table.column(col, width=100, anchor="center")
        self.compare_table.pack(fill="x")

    # ---------- data helpers ----------
    def _refresh_table(self):
        self.table.delete(*self.table.get_children())
        for p in self.processes:
            self.table.insert("", "end", values=(p.pid, p.arrival, p.burst))

    def _load_sample(self):
        try:
            self.processes = load_processes_csv(
                os.path.join(BASE_DIR, "input", "sample_01.csv"))
        except Exception:
            self.processes = [Process("P1", 0, 5), Process("P2", 1, 3)]
        self._refresh_table()

    def add_process(self):
        try:
            p = Process(self.e_pid.get().strip(),
                        int(self.e_arr.get()), int(self.e_burst.get()))
            if not p.pid or p.burst <= 0 or p.arrival < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input",
                                 "Check pid / arrival (>=0) / burst (>0).")
            return
        self.processes.append(p)
        self._refresh_table()

    def remove_process(self):
        sel = self.table.selection()
        if sel:
            idx = self.table.index(sel[0])
            self.processes.pop(idx)
            self._refresh_table()

    def load_csv(self):
        path = filedialog.askopenfilename(
            initialdir=os.path.join(BASE_DIR, "input"),
            filetypes=[("CSV files", "*.csv")])
        if path:
            self.processes = load_processes_csv(path)
            self._refresh_table()

    def save_csv(self):
        if not self.last_result:
            messagebox.showinfo("Nothing to save", "Run the simulation first.")
            return
        path = filedialog.asksaveasfilename(
            initialdir=os.path.join(BASE_DIR, "output"),
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            save_results_csv(path, self.last_result)

    # ---------- simulation ----------
    def run(self):
        if not self.processes:
            messagebox.showinfo("No processes", "Add at least one process.")
            return
        r = simulate_round_robin(self.processes, self.var_q.get(),
                                 self.var_cs.get())
        self.last_result = r
        self.results.delete(*self.results.get_children())
        for x in r.per_process:
            self.results.insert("", "end", values=(
                x.pid, x.arrival, x.burst, x.completion,
                x.turnaround, x.waiting, x.response))
        self.lbl_summary.config(text=(
            f"Avg waiting: {r.avg_waiting:.2f}   "
            f"Avg turnaround: {r.avg_turnaround:.2f}   "
            f"Avg response: {r.avg_response:.2f}   "
            f"Context switches: {r.context_switches}   "
            f"Overhead: {r.overhead_time}   Total time: {r.total_time}"))
        self._draw_gantt(r)

    def _draw_gantt(self, r):
        c = self.gantt
        c.delete("all")
        width = max(int(c.winfo_width()), 600)
        unit = (width - 20) / max(r.total_time, 1)
        color = {p.pid: COLORS[i % len(COLORS)]
                 for i, p in enumerate(self.processes)}
        for s in r.segments:
            x0, x1 = 10 + s.start * unit, 10 + s.end * unit
            fill = ("#dddddd" if s.pid == "IDLE" else
                    "#999999" if s.pid == "CS" else color.get(s.pid, "#cccccc"))
            c.create_rectangle(x0, 15, x1, 55, fill=fill, outline="black")
            if x1 - x0 > 16:
                c.create_text((x0 + x1) / 2, 35, text=s.pid)
            c.create_text(x0, 68, text=str(s.start))
        c.create_text(10 + r.total_time * unit, 68, text=str(r.total_time))

    def compare(self):
        if not self.processes:
            return
        try:
            quanta = [int(x) for x in self.e_quanta.get().split(",")
                      if x.strip()]
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
